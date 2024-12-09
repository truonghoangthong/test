from django.contrib import admin
from .models import Bus, Metro, Ticket, Account, User, UserTicket, AccountHasUser, Image,FavPlace

admin.site.register(Ticket)
admin.site.register(Image)
admin.site.register(FavPlace)


#create superuser to access admin page
'''
python manage.py createsuperuser
python manage.py runserver
'''

