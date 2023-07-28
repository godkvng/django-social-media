from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect

from .models import Profile


def index(request):
	context = {}
	return render(request, 'core/index.html', context)


def sign_in(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Invalid login credentials')
			return redirect('sign-in')
	else:
		context = {}
		return render(request, 'core/signin.html', context)


def sign_up(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']

		if password1 == password2:
			if User.objects.filter(email=email).exists():
				messages.info(request, "Email address already exists")
				return redirect('sign-up')
			elif User.objects.filter(username=username).exists():
				messages.info(request, "Username already taken")
				return redirect('sign-up')
			else:
				user = User.objects.create_user(username=username, email=email, password=password1)
				user.save()

				# Create a profile object for the new user
				user_model = User.objects.get(username=username)
				user_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
				user_profile.save()
				return redirect('login')
		else:
			messages.info(request, "Passwords do not match")
			return redirect('sign-up')
	context = {}
	return render(request, 'core/signup.html', context)
