from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings

# Authen API
import json
from .models import User
from .serializers import UserLoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from .models import Image
from django.shortcuts import get_object_or_404
import os

# Ticket list
from .models import Ticket

# Email
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


#Get route/ map API
def get_route(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf62481c184721ac24419cbc62a1f87c43d9dc&start={start}&end={end}"
# syntax: &start = {start} & end = {end}
# test location: &start=105.883999,21.049659&end=105.855546,21.024705
    respond = requests.get(url) # Request API from this

    if respond.status_code == 200:
        return JsonResponse(respond.json()) #Return json data
    else:
        return JsonResponse({'error': respond.status_code})


#Login
class UserLoginView(APIView):
    def post(self, request):
        try: # from here
            if request.content_type == 'application/json':
                data = request.data
            else:
                raw_body = request.POST.get('_content')
                if raw_body:
                    data = json.loads(raw_body)
                else:
                    return Response(
                        {"error": "Invalid content-type or missing data."},
                        status=status.HTTP_400_BAD_REQUEST
                    )  # to here. Warning: cấm xóa,cấm sửa chó nào đụng t chặt tay. 

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

#Sign up
@api_view(['POST'])
def signup(request):
    try: # from here
        if request.content_type == 'application/json':
            data = request.data
        else:
            raw_body = request.POST.get('_content')
            if raw_body:
                data = json.loads(raw_body)
            else:
                return Response(
                    {"error": "Invalid content-type or missing data."},
                    status=status.HTTP_400_BAD_REQUEST
                )  # to here. Warning: cấm xóa,cấm sửa chó nào đụng t chặt tay. 

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


#Ticket list
def ticketList(request):
    tickets = Ticket.objects.all()
    return render(request, 'virouteapp/ticket_list.html', {'tickets': tickets})

#Image 
def get_image_by_name(request, image_name):
    image = get_object_or_404(Image, image_name=image_name)
    
    if not image.image_path:
        return HttpResponse("Image does not exist", status=404)
    
    image_path = os.path.join(settings.MEDIA_ROOT, 'images', image.image_path.name)


    with open(image_path, 'rb') as img:
        return HttpResponse(img.read(), content_type="image/png")
    
@api_view(['PUT'])
def update_user_info(request, user_id):
    try:# from here
        try:
            user = User.objects.get(userID=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.content_type == 'application/json':
            data = request.data
        else:
            raw_body = request.POST.get('_content')
            if raw_body:
                data = json.loads(raw_body)
            else:
                return Response(
                    {"error": "Invalid content-type or missing data."},
                    status=status.HTTP_400_BAD_REQUEST
                ) # to here. Warning: cấm xóa,cấm sửa chó nào đụng t chặt tay. 
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User updated successfully",
                    "user": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {"error": "An unexpected error occurred", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(['POST'])
def forgot_password(request):
    try: # from here
        if request.content_type != 'application/json':
            data = request.data

        else:
            raw_body = request.POST.get('_content')
            if raw_body:
                data = json.loads(raw_body)
            else:
                return Response(
                    {"error": "Invalid content-type or missing data."},
                    status=status.HTTP_400_BAD_REQUEST
                ) # to here. Warning: cấm xóa,cấm sửa chó nào đụng t chặt tay. 
        email = data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email not found."}, status=status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(user)

        uid = urlsafe_base64_encode(user.pk.encode())
        reset_link = f"http://localhost:5173/reclaimpass/{uid}/{token}/"

        send_mail(
            "Thằng scrum master ngu ngốc",
            f"Click the link to reset your password: {reset_link}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)

    except Exception as e: 
            return Response(
                {"error": "An error occurred", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )



@api_view(['PUT'])
def reset_password(request, uidb64, token):
    try:# from here
        if request.content_type != 'application/json':
            data = request.data

        else:
            raw_body = request.POST.get('_content')
            if raw_body:
                data = json.loads(raw_body)
            else:
                return Response(
                    {"error": "Invalid content-type or missing data."},
                    status=status.HTTP_400_BAD_REQUEST
                ) # to here. Warning: cấm xóa,cấm sửa chó nào đụng t chặt tay. 

        new_password = data.get('password')

        if not new_password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response({"error": "Invalid link or user not found."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password successfully updated."}, status=status.HTTP_200_OK)
    except Exception as e:
            return Response(
                {"error": "An error occurred", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
