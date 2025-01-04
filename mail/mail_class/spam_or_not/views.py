from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
import base64
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use a different email.')
                return redirect('spam_or_not:signup') 
            else:
                user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
                login(request, user)
                return redirect('spam_or_not:login')  
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('spam_or_not:home')  
        else:
            messages.error(request, "Invalid credentials")
            return redirect('spam_or_not:login')
    else:
        return render(request, 'login.html')
    
def home(request):
    return render(request, 'home.html')


from django.shortcuts import render
from .utils import train_model, predict_email_type

def home(request):
    feature_extraction, lg_model,label_encoder = train_model()
    
    if request.method == 'POST':
        input_mail = request.POST.get('email', '')
        prediction = predict_email_type(input_mail, feature_extraction, lg_model)
        prediction_label = label_encoder.inverse_transform(prediction)[0]
        context = {'prediction': prediction_label}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')

