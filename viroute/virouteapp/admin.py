from django.contrib import admin
from .models import Bus, Metro, Ticket, Account, User, UserTicket, AccountHasUser, Image

admin.site.register(Ticket)
admin.site.register(Image)

#create superuser to access admin page
'''
python manage.py createsuperuser
python manage.py runserver
'''

