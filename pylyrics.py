#!/usr/bin/python2

import requests
import urllib
from bs4 import BeautifulSoup
import re
import time
import subprocess
from bisect import *
import sys
import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def getTTYSize():
	return map(int, os.popen('stty size', 'r').read().split())

oldArtist,oldTitle = [None]*2



def getSongInfo():
	title = subprocess.check_output(['playerctl', 'metadata', 'title'])
	artist = subprocess.check_output(['playerctl', 'metadata', 'artist'])
	time_elapsed = int(float(subprocess.check_output(['playerctl', 'position'])))
	return title, artist, time_elapsed

def getGoogle(title,artist):
	headers = {
	    'User-Agent': 'Mozilla/5.0',
	}
	query = "%s %s site:rentanadviser.com" % (title, artist)
	params = (
	    ('tbs', 'li:1'),
	    ('q', '+'.join(query.split(' '))),
	)

	response = requests.get('https://www.google.com/search', headers=headers, params=params, verify=False)
	result = re.findall('href=\"/url\?q=.*?&amp', response.text)[0][len('href="/url?q='):-len('&amp')]
	result = urllib.unquote(result)
	return result

def time_to_secs(string):
	string = re.split('[\[\]\:\.]', string)
	secs = int(string[1],10)*60 + int(string[2], 10)
	return secs

def print_lyrics(line):
	columns, rows = getTTYSize()
	lne = ((rows-len(line))/2)*' ' + line
	sys.stdout.write('%s%s\r' % (lne, (rows-len(lne))*' ' ))
	sys.stdout.flush()

def getsyncedLyrics(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')

	eventTarget = urllib.unquote('ctl00%24ContentPlaceHolder1%24btnlyricssimple')

	data = {
		'__EVENTTARGET' : eventTarget,
		'__EVENTARGUMENT' : '',
	 	'ctl00$txtSearch' : 'Search Apps...',
	 	'ctl00$Overcome_Enter_problem_in_IE1' : '',
	 	'ctl00$ContentPlaceHolder1$txtsearchsubtitle' : 'Search Subtitle...',
	 	'ctl00$ContentPlaceHolder1$Overcome_Enter_problem_in_IE2' : '',
	}

	for inp in soup.find_all(id=re.compile('__.*')):
		data[inp.get('name')] = inp.get('value')

	resp = requests.post(url, data=data)

	lyrics = resp.text.replace('\r', '\n').replace('\n\n','\n').strip().split('\n')[1:-1]
	
	timeLine = []
	lyricLine = []
	for line in lyrics:
		timeString =  re.findall('^\[.*?\]', line)[0]
		timeLine.append(time_to_secs(timeString))
		lineString = re.sub('^.*?\]', '\n', line).strip()
		lyricLine.append(lineString)
	return timeLine,lyricLine	
def display_lyrics(full_lyrics, time_elapsed):
	times, lyrics = full_lyrics
	i = bisect_right(times, time_elapsed)
	if i:
		print_lyrics(lyrics[i-1])
	else:
		print_lyrics('')

url=lyrics=None
while True:
	currentTitle, currentArtist, time_elapsed = getSongInfo()

	if currentArtist!=oldArtist and currentTitle!=oldTitle:
		if currentTitle=='' or currentArtist=='':
			print_lyrics('...Waiting for song...')
			time.sleep(0.5)
			continue
		url = getGoogle(currentTitle, currentArtist)
		lyrics = getsyncedLyrics(url)

	display_lyrics(lyrics, time_elapsed)
	time.sleep(0.5)
	oldArtist=currentArtist
	oldTitle=currentTitle