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

def index(request):
    return render(request, "index.html", context={'session': dict(request.session)})


def stations(request):
    result = SearchStationsCommand(request).execute()
    return result



def signup(request):
    result = SignupCommand(request).execute()
    return result



def login(request):
    result = LoginCommand(request).execute()
    return result


def logout(request):
    result = LogoutCommand().execute()
    return result



def send_password_reset(request):
    result = SendPasswordResetCommand(request).execute()
    return result



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



def orders(request):
    if request.method == 'GET':
        result = ReadOrdersCommand().execute()

    if request.method == 'POST':
        result = CreateOrderCommand(request).execute()
    
    return result



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
    return redirect('index')


def handle_500(request):
    return redirect('index')
