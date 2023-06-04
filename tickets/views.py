from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.db import connections
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from waitress import serve
from dotenv import load_dotenv
from tickets.database import *
from tickets.command import *
import pdfkit

load_dotenv()

public_url = f"{settings.DOMAIN}"

database_type = settings.DATABASE_TYPE

database = DatabaseList().get_database(database_type)

carriage_table = database.get_table('carriage')
carriage_type_table = database.get_table('carriage_type')
seat_table = database.get_table('seat')
station_table = database.get_table('station')
ticket_table = database.get_table('ticket')
train_table = database.get_table('train')
trip_table = database.get_table('trip')
trip_station_table = database.get_table('trip_station')
user_table = database.get_table('user')
user_role_table = database.get_table('user_role')

tables = {
    'carriage': carriage_table,
    'carriage_type': carriage_type_table,
    'seat': seat_table,
    'station': station_table,
    'ticket': ticket_table,
    'train': train_table,
    'trip': trip_table,
    'trip_station': trip_station_table,
    'user': user_table,
    'user_role': user_role_table
}

app = get_wsgi_application()

app.secret_key = b'yb4No3!w2NX528'

def index(request):
    return render(request, "index.html")


def stations(request):
    result = SearchStationsCommand(request).execute()
    return result


@csrf_exempt
def signup(request):
    result = SignupCommand(request).execute()
    return result


@csrf_exempt
def login(request):
    result = LoginCommand(request).execute()
    return result


def logout(request):
    result = LogoutCommand().execute()
    return result


@csrf_exempt
def send_password_reset(request):
    result = SendPasswordResetCommand(request).execute()
    return result


@csrf_exempt
def reset_password(request):
    if request.method == 'GET':
        return render(request, "reset_password.html")
        
    if request.method == 'POST':
        result = ResetPasswordCommand(request).execute()
    
    return result


def profile(request):
    if request.method == 'GET':
        result = ReadProfileCommand().execute()
        
    if request.method == 'PATCH':
        result = UpdateProfileCommand(request).execute()
    
    return result


def admin(request):
    result = ReadUsersCommand().execute()
    return result


def search(request):
    result = SearchTicketsCommand(request).execute()
    return result


def seats(request):
    result = SearchSeatsCommand(request).execute()
    return result


@csrf_exempt
def orders(request):
    if request.method == 'GET':
        result = ReadOrdersCommand().execute()

    if request.method == 'POST':
        result = CreateOrderCommand(request).execute()
    
    return result


@csrf_exempt
def payment_completed(request):
    result = CompleteOrderCommand(request).execute()
    return result


def verify(request):
    result = VerifyOrderCommand(request).execute()
    return result


def create_qrcode(request):
    result = CreateQrcodeCommand(request).execute()
    return result


def confirm_account(request):
    result = ConfirmAccountCommand(request).execute()
    return result
    

def handle_404(request, exception):
    return redirect(reverse('index'))


def handle_500(request):
    return redirect(reverse('index'))
