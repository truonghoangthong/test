from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
import json
from .models import User, Ticket, Image
from .serializers import UserLoginSerializer, UserSerializer, BusRouteSerializer
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
# Ticket list
from .models import Ticket, BusRoute



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
    return render(request, 'ticket_list.html', {'tickets': tickets})


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

@api_view(['GET'])
def get_bus_routes(request):
    bus_routes = BusRoute.objects.all()
    serializer = BusRouteSerializer(bus_routes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_bus_routes_by_start_and_end(request):
    bus_start = request.data.get('bus_start', None)
    bus_end = request.data.get('bus_end', None)
    
    if not bus_start or not bus_end:
        return Response(
            {"error": "bus_start and bus_end are required fields."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    bus_routes = BusRoute.objects.filter(
        bus_start__icontains=bus_start, 
        bus_end__icontains=bus_end
    )
    
    bus_names = bus_routes.values_list('bus_Name', flat=True)
    
    if not bus_names:
        return Response(
            {"message": "No bus routes found for the given start and end points."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response({"bus_names": list(bus_names)}, status=status.HTTP_200_OK)








