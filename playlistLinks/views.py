# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404,render
from django.template import loader
from django.urls import reverse
from .models import User,Links
from datetime import datetime
from . import calculations as c

def home(request):
	# cities = {'cities': ['Chicago','Boston']}
	return render(request,'playlistLinks/home.html')

def getData(request):
	try:
		email = request.POST.get('email','nothing')
		city = request.POST.get('city',False)
		links = request.POST.get('links','')

		links = [x.strip() for x in links.split(',')]

		if email == 'nothing' or '@' not in email:
			return render(request,'playlistLinks/links.html',{'error_message':"Did not enter valid email"})
		if not city or city == '':
			return render(request,'playlistLinks/links.html',{'error_message':"Did not select a city"})
		if links[0] == '':
			return render(request,'playlistLinks/links.html',{'error_message':"Did not give a proper link"})
	except KeyError as e:
		print(e)
		return render(request,'playlistLinks/links.html',{'error_message':"Something went wrong, try again"})

	#adding to database if doesn't already exist
	try:
		u = User.objects.get(email=email)
	except User.DoesNotExist:
		u = User(email=email,create_date = datetime.today(),city=city)
		u.save()
	user_artists = c.getArtists(links)
	#user_concerts = c.getUsersConcerts(city,user_artists,180)
	c.addArtistsToDB(u,user_artists)
	c.addLinksToDB(u,links)
	#c.sftp('db.sqlite3','/emailer/')
	return HttpResponseRedirect(reverse('playlistLinks:concerts',args=(u.id,)))

def concerts(request,user_id):
	u = get_object_or_404(User,pk=user_id)
	user_artists = u.artist_set.all()
	print(len(user_artists))
	user_concerts = c.getUsersConcerts(u.city,user_artists)
	return render(request,'playlistLinks/concerts.html',{'concerts':user_concerts})

def inputForDelete(request):
	return render(request,'playlistLinks/delete.html')

def delete(request):
	user = get_object_or_404(User,email=request.POST.get('email','nothing'))
	user_id = user.id
	try:
		User.objects.filter(id=user_id).delete()
	except User.DoesNotExist:
		return render(request,'playlistLinks/home.html')
	return HttpResponseRedirect(reverse('playlistLinks:deleteDone',args=(user_email,)))

def deleteDone(request,email):
	return render(request,'playlistLinks/deleted.html',{'email':email})

def getConcerts(request):
	try:
		email = request.POST.get('email','nothing')
		if email == 'nothing' or '@' not in email:
			return render(request,'playlistLinks/getConcerts.html',{'error_message':"Did not enter valid email"})
	except KeyError as e:
		return render(request,'playlistLinks/links.html',{'error_message':"Something went wrong, try again"})
	user = get_object_or_404(User,email=email)
	user_id = user.id
	return HttpResponseRedirect(reverse('playlistLinks:concerts',args=(user.id,)))

def inputForConcerts(request):
	return render(request,'playlistLinks/getConcerts.html')

def updateAllConcerts(request,city):
	c.addConcertsToDB(city)
	return render(request,'playlistLinks/updated.html')

