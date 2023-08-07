from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Profile, Post


@login_required(login_url='sign-in')
def index(request):
	user_object = User.objects.get(username=request.user.username)
	user_profile = Profile.objects.get(user=user_object)
	posts = Post.objects.all()
	context = {
		'user_profile': user_profile.save,
		'posts': posts,
	}
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

				user_login = auth.authenticate(username=username, password=password1)
				auth.login(request, user_login)

				# Create a profile object for the new user
				user_model = User.objects.get(username=username)
				user_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
				user_profile.save()
				return redirect('settings')
		else:
			messages.info(request, "Passwords do not match")
			return redirect('sign-up')
	context = {}
	return render(request, 'core/signup.html', context)


@login_required(login_url='sign-in')
def log_out(request):
	auth.logout(request)
	return redirect('sign-in')


@login_required(login_url='sign-in')
def settings(request):
	user_profile = Profile.objects.get(user=request.user)

	if request.method == 'POST':
		if request.FILES.get('image') is not None:
			image = request.FILES.get('image')
			bio = request.POST['bio']
			location = request.POST['location']

			user_profile.profileimg = image
			user_profile.bio = bio
			user_profile.location = location
			user_profile.save()
		else:
			image = user_profile.profileimg
			bio = request.POST['bio']
			location = request.POST['location']

			user_profile.profileimg = image
			user_profile.bio = bio
			user_profile.location = location
			user_profile.save()
		return redirect('settings')

	context = {
		'user_profile': user_profile
	}
	return render(request, 'core/setting.html', context)


@login_required(login_url='sign-in')
def upload(request):
	if request.method == 'POST':
		user = request.user.username
		image = request.FILES.get('image-upload')
		caption = request.POST['caption']

		new_post = Post.objects.create(user=user, image=image, caption=caption)
		new_post.save()
		return redirect('home')
	else:
		return redirect('home')
