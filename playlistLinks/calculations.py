from datetime import datetime, timedelta
import pytz
import requests
from bs4 import BeautifulSoup
import ast
import re
import pickle
from . import get_concerts as gc
from .models import Artist,Links,Concert,Update
import os
import pysftp

def getArtists(ls):
	all_artists = []
	for l in ls:
		page = requests.get(l)
		soup = BeautifulSoup(page.content,'html.parser')
		main = soup.find(id="main")
		#z = soup.find_all(class_="artist_name") 
		x = soup.find_all("script")
		y = str(x[5])
		z = y.split(';')
		d = z[1].lstrip()
		all_artists += re.findall(r'\"name\":\"(.+?)\"',d)
	return list(set(all_artists))

def getConcerts(city):
	last_update = Update.objects.filter(city=city)[0]
	today = datetime.today()
	utc=pytz.UTC
	file_name = 'playlistLinks/all_concerts_%s.pickle' % city
	with open(file_name,'rb') as f:
		all_concerts = pickle.load(f,encoding="utf-8")
	f.close()
	return all_concerts

def getUsersConcerts(city,artists):
	every_concert = getConcerts(city)
	matches = []
	print(len(every_concert.keys()))
	for artist in artists:
		try:
			(date,loc) = every_concert[artist.name]
			d = datetime.strptime(date, '%m%d%Y') # changed #have to convert to date object to sort them
			if d >= datetime.today():
				matches += [(d,artist.name,loc)]        
		except KeyError as e:
	#print(e)
			continue
	matches_sorted = sorted(matches)
	matches_list_final = []
	for x in matches_sorted:
		(d,a,l) = x
		matches_list_final += [(d.strftime('%m-%d-%Y'),a,l)] #added the dashes
		concert_list = []
	for (date,artist,location) in matches_list_final:
		concert_list.append('%s--%s--%s' % (artist,location,date)) #removed the \n from the end
		#print(artist + '--' + location + '--' + date)
	return concert_list

def addArtistsToDB(user,artists):
	for artist in artists:
		try:
			a = Artist.objects.get(name=artist)
			try:
				a = Artist.objects.get(name=artist,users=user)
			except Artist.DoesNotExist:
				a.users.add(user) 
				a.save()
		except Artist.DoesNotExist as e:
			a = Artist(name=artist)
			a.save()
			a.users.add(user)
			a.save()
	return

def addLinksToDB(user,links):
	for link in links:
		try:
			l = Links.objects.get(url=link)
			try:
				l = Links.objects.get(url=link,users=user)
			except Links.DoesNotExist:
				l.users.add(user)
				l.save()
		except Links.DoesNotExist:
			l = Links(url=link)
			l.save()
			l.users.add(user)
			l.save()
	return

def addConcertsToDB(c):
	concerts = getConcerts(c)
	for key in concerts.keys():
		(d,v) = concerts[key]
		d = datetime.strptime(d,'%m%d%Y')
		d2 = d.strftime('%m-%d-%Y')
		try:
			Concert.objects.get(band=key)
		except Concert.DoesNotExist:
			d = datetime.strptime(d2,'%m-%d-%Y')
			c = Concert(band=key,venue=v,concert_date=d,city=c)
			c.save()
	return

def sftp(db_name,rp):
	srv = pysftp.Connection(host=os.environ['HOST'],username=os.environ['USERNAME'],password=os.environ['PASSWORD_OCEAN'])
	srv.put(db_name)
	srv.close()
	return

