from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings

# xóa 1 đống ở đây nha Dung nha :)
# Authen API
import bcrypt
import json
from .models import User
from .serializers import UserLoginSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from .models import Image
from django.shortcuts import get_object_or_404
import os




#Ticket list
from .models import Ticket


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
        try:
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
                    )

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
    try:
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
                )

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
    try:
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
                )
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