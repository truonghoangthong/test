from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
import json
from .models import User, Ticket, Image
from .serializers import UserLoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import os
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import yagmail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)


# Get route/map API
def get_route(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf62481c184721ac24419cbc62a1f87c43d9dc&start={start}&end={end}"
    response = requests.get(url)

    if response.status_code == 200:
        return JsonResponse(response.json())  # Return JSON data
    else:
        return JsonResponse({'error': response.status_code})


# Login
class UserLoginView(APIView):
    def post(self, request):
        try:
            data = request.data  # Expecting JSON body from the client

            print("Parsed data:", data)

            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                return Response({
                    "message": "Login successful",
                    "user": {
                        "userID": user.userID,
                        "fullName": user.fullName,
                        "userEmail": user.userEmail,
                        "balance": str(user.balance)
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                "message": "Login failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "An error occurred", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# Sign up
@api_view(['POST'])
def signup(request):
    try:
        data = request.data  # Expecting JSON body

        print("Parsed data:", data)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "userID": user.userID,
                    "fullName": user.fullName,
                    "userEmail": user.userEmail,
                    "balance": str(user.balance)
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": "An error occurred", "details": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# Ticket list
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'virouteapp/ticket_list.html', {'tickets': tickets})


# Get image by name
def get_image_by_name(request, image_name):
    image = get_object_or_404(Image, image_name=image_name)

    if not image.image_path:
        return HttpResponse("Image does not exist", status=404)

    image_path = os.path.join(settings.MEDIA_ROOT, 'images', image.image_path.name)

    with open(image_path, 'rb') as img:
        return HttpResponse(img.read(), content_type="image/png")


# Update user information
@api_view(['PUT'])
def update_user_info(request, user_id):
    try:
        try:
            user = User.objects.get(userID=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data  # Expecting JSON body

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": "An unexpected error occurred", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Forgot password
def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def send_reset_email(email, reset_link):
    subject = "Password Reset"
    message = f"Click the link to reset your password: {reset_link}"
    from_email = 'your_email@gmail.com'

    try:
        # Use yagmail to send the reset email
        yag = yagmail.SMTP(from_email, 'your_email_password')
        yag.send(to=email, subject=subject, contents=message)
        logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise Exception(f"Failed to send email: {str(e)}")

# Forgot Password API (POST)
@api_view(['POST'])
def forgot_password(request):
    try:
        data = request.data
        email = data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the email format
        if not is_valid_email(email):
            return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email exists
        try:
            user = User.objects.get(userEmail=email)
        except User.DoesNotExist:
            # Không gửi email nếu email không tồn tại
            return Response({"message": "If an account exists with this email, a reset link has been sent."}, 
                             status=status.HTTP_200_OK)  # Trả lời thành công, nhưng không tiết lộ có hay không tài khoản

        # Generate reset token and link
        token_generator = CustomPasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())
        reset_link = f"http://localhost:5173/reclaimpass/{uid}/{token}/"

        # Send the reset email
        send_reset_email(user.userEmail, reset_link)
        logger.info(f"Password reset email sent to: {email}")

        return Response({"message": "If an account exists with this email, a reset link has been sent."}, 
                         status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in forgot_password: {e}")
        return Response({"error": "An error occurred while processing your request."}, 
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Reset Password API (PUT)
@api_view(['PUT'])
def reset_password(request, uidb64, token):
    """
    Reset password based on the token and UID.
    """
    new_password = request.data.get('password')

    if not new_password:
        return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Decode the UID and get the user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        return Response({"error": "Invalid link or user not found."}, status=status.HTTP_404_NOT_FOUND)

    # Verify the token
    token_generator = CustomPasswordResetTokenGenerator()
    if not token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

    # Reset the password
    user.set_password(new_password)
    user.save()

    return Response({"message": "Password successfully updated."}, status=status.HTTP_200_OK)

# CSRF Token API
@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)  # CSRF token from middleware
    return Response({'csrf_token': csrf_token})

# Custom Password Reset Token Generator
class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Use current timestamp instead of last_login
        login_timestamp = now()
        return f"{user.pk}-{login_timestamp}-{user.email}"
        
