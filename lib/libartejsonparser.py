# -*- coding: utf-8 -*-
import json
import libmediathek3 as libMediathek
import re
import urllib
from operator import itemgetter
#import xml.etree.ElementTree as ET

	
def getVideos(url):
	l = []
	response = libMediathek.getUrl(url)
	j = json.loads(response)
	for video in j['videos']:
		d = {}
		#d['_name'] = video['title']
		if video['subtitle'] != None:
			d['_name'] = video['subtitle']
		else:
			d['_name'] = video['title']
		
		d['_tvshowtitle'] = video['title']
		if video['imageUrl'] != None:
			d['_thumb'] = video['imageUrl']
		if video['teaserText'] != None:
			d['_plotoutline'] = video['teaserText']
			d['_plot'] = video['teaserText']
		if video['fullDescription'] != None:
			d['_plot'] = video['fullDescription']
		elif video['shortDescription'] != None:
			d['_plot'] = video['shortDescription']
		#d['url'] = 'http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/streams/'+video['programId']+'/'+video['kind']+'/'+video['platform']+'/de/DE'
		d['url'] = 'https://api.arte.tv/api/player/v1/config/de/'+video['programId']+'?autostart=0&lifeCycle=1&lang=de_DE&config=arte_tvguide'
		d['mode'] = 'libArteSelectLang'
		d['_type'] = 'dir'
		l.append(d)
	if j['meta']['page'] < j['meta']['pages']:
		d = {}
		d['url'] = url.split('&page=')[0] + '&page=' + str(j['meta']['page'] + 1)
		d['_type'] = 'nextPage'
		d['mode'] = 'libArteListVideos'
		l.append(d)
	return l

def getAZ():
	l = []
	response = libMediathek.getUrl('http://www.arte.tv/hbbtvv2/services/web/index.php/EMAC/teasers/home/de')
	j = json.loads(response)
	for mag in j['teasers']['magazines']:
		d = {}
		d['_name'] = mag['label']['de']
		d['url'] = 'http://www.arte.tv/hbbtvv2/services/web/index.php/' + mag['url'] + '/de'
		d['_type'] = 'dir'
		d['mode'] = 'libArteListVideos'
		l.append(d)
	return l
	
def getPlaylists():#,playlists, highlights
	l = []
	response = libMediathek.getUrl('http://www.arte.tv/hbbtvv2/services/web/index.php/EMAC/teasers/home/de')
	j = json.loads(response)
	for playlist in j['teasers']['playlists']:
		d = {}
		d['_name'] = playlist['title']
		d['_subtitle'] = playlist['subtitle']
		d['_thumb'] = playlist['imageUrl']
		d['_plot'] = playlist['teaserText']
		d['url'] = 'http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/v3/videos/collection/PLAYLIST/' + playlist['programId'] + '/de'
		d['_type'] = 'dir'
		d['mode'] = 'libArteListVideos'
		l.append(d)
	return l
		
	
	
def getDate(yyyymmdd):
	l = []
	response = libMediathek.getUrl('http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/programs/'+yyyymmdd+'/de')
	j = json.loads(response)
	for program in j['programs']:
		if program['video'] != None:
			d = {}
			#d['_airedtime'] = program['broadcast']['broadcastBeginRounded'].split(' ')[-2][:5]
			s = program['broadcast']['broadcastBeginRounded'].split(' ')[-2].split(':')
			d['_airedtime'] = str(int(s[0]) + 1) + ':' + s[1]
			if len(d['_airedtime']) == 4:
				d['_airedtime'] = '0' + d['_airedtime']
			d['_name'] = program['program']['title']
			#d['url'] = 'http://www.arte.tv/papi/tvguide/videos/stream/player/D/'+program['video']['emNumber']+'_PLUS7-D/ALL/ALL.json'
			#d['url'] = 'http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/streams/'+program['video']['programId']+'/SHOW/ARTEPLUS7/de/DE'
			#d['url'] = 'http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/streams/'+program['video']['programId']+'/'+program['video']['kind']+'/'+program['video']['platform']+'/de/DE'
			
			d['url'] = 'https://api.arte.tv/api/player/v1/config/de/'+program['video']['programId']+'?autostart=0&lifeCycle=1&lang=de_DE&config=arte_tvguide'
			#d['programId'] = program['video']['programId']
			
			if program['video']['imageUrl'] != None:
				d['_thumb'] = program['video']['imageUrl']
			if program['video']['teaserText'] != None:
				d['_plotoutline'] = program['video']['teaserText']
				d['_plot'] = program['video']['teaserText']
			if program['video']['fullDescription'] != None:
				d['_plot'] = program['video']['fullDescription']
			d['mode'] = 'libArteSelectLang'
			d['_type'] = 'dir'
			l.append(d)
	return l

def getSearch(s):
	l = []
	url = 'http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/v3/videos/search/text/'+urllib.quote_plus(s)+'/de'
	response = libMediathek.getUrl(url)
	j = json.loads(response)
	for video in j['teasers']:
		d = {}
		d['_name'] = video['title']
		
		d['_tvshowtitle'] = video['title']
		if video['imageUrl'] != None:
			d['_thumb'] = video['imageUrl']
		d['url'] = 'https://api.arte.tv/api/player/v1/config/de/'+video['programId']+'?autostart=0&lifeCycle=1&lang=de_DE&config=arte_tvguide'
		d['mode'] = 'libArteSelectLang'
		d['_type'] = 'dir'
		if video['shortDescription'] != None:
			d['_plot'] = video['shortDescription']
		l.append(d)
	return l

def selectLang(url):
	l = []

	response = libMediathek.getUrl(url)
	j = json.loads(response)
	for key in j['videoJsonPlayer']['VSR']:
		if j['videoJsonPlayer']['VSR'][key]['mediaType'] == 'hls':
			d = {}
			d['_name'] = j['videoJsonPlayer']['VSR'][key]['versionLibelle']
			d['title'] = j['videoJsonPlayer']['VTI']
			d['_tvshowtitle'] = j['videoJsonPlayer']['VSR'][key]['versionLibelle'] + 'Q'
			d['_thumb'] = j['videoJsonPlayer']['VTU']['IUR']
			d['thumb'] = j['videoJsonPlayer']['VTU']['IUR']
			if 'VDE' in j['videoJsonPlayer']:
				d['_plot'] = j['videoJsonPlayer']['VDE']
				d['plot'] = j['videoJsonPlayer']['VDE']
			elif 'V7T' in j['videoJsonPlayer']:
				d['_plot'] = j['videoJsonPlayer']['V7T']
				d['plot'] = j['videoJsonPlayer']['V7T']
			d['_duration'] = str(j['videoJsonPlayer']['videoDurationSeconds'])
			d['duration'] = str(j['videoJsonPlayer']['videoDurationSeconds'])
			d['_type'] = 'date'
			d['mode'] = 'libArtePlay'
			d['url'] = j['videoJsonPlayer']['VSR'][key]['url']
			l.append(d)
	return l

def getVideoUrlWeb(url,title,plot,thumb,duration):
	d = {}
	d['media'] = []
	d['media'].append({'url':url, 'type':'video', 'stream':'HLS'})
	d['metadata'] = {'name':title, 'plot':plot, 'thumb':thumb, 'duration':duration}
	return d