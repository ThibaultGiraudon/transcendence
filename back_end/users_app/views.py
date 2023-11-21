from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, SignUpForm

def sign_in(request):
	if request.method == 'GET':
		form = LoginForm()
		return render(request, 'users/sign_in.html', {'form': form})
	
	elif request.method == 'POST':
		form = LoginForm(request.POST)
		
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request,username=username, password=password)
			if user:
				login(request, user)
				return redirect('pong')
			else:
				messages.error(request, "Invalid credentials")
				return redirect('sign_in')

		messages.error(request, "Form error, you need to provide all fields")
		return redirect('sign_in')


def sign_up(request):
	if request.method == 'GET':
		form = SignUpForm()
		return render(request, 'users/sign_up.html', {'form': form})
	
	elif request.method == 'POST':
		form = SignUpForm(request.POST)
		
		if form.is_valid():
			user = User.objects.create_user(
					username=form.cleaned_data['username'],
					email=form.cleaned_data['email'],
					password=form.cleaned_data['password'])
			user.save()
			return redirect('sign_in')
	
	messages.error(request, "Form error")
	return redirect('sign_up')


def sign_out(request):
    # Logout the current user
	if request.user.is_authenticated:
		logout(request)
	
	return redirect('sign_in')
