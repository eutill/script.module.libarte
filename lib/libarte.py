# -*- coding: utf-8 -*-
import sys
import urllib
import libartejsonparser as libArteJsonParser
import libmediathek3 as libMediathek

translation = libMediathek.getTranslation


def libArteListMain():
	l = []
	l.append({'_name':translation(31031), 'mode':'libArteListVideos',	'_type':'dir', 'url':'http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/videos/mostviewed/20/ARTEPLUS7/de/DE'})
	l.append({'_name':translation(31032), 'mode':'libArteListShows',  	'_type':'dir'})
	l.append({'_name':translation(31033), 'mode':'libArteListDate',		'_type':'dir'})
	l.append({'_name':translation(31035), 'mode':'libArteThemes',		'_type':'dir'})
	l.append({'_name':translation(31039), 'mode':'libArteSearch', 		'_type':'dir'})
	return l
	
def libArteListShows():
	return libArteJsonParser.getAZ()
	
def libArteThemes():
	return libArteJsonParser.getPlaylists()
	
def libArteListVideos():
	return libArteJsonParser.getVideos(params['url'])

def libArteListDate():
	return libMediathek.populateDirDate('libArteListDateVideos')
		
def libArteListDateVideos():
	return libArteJsonParser.getDate(params['yyyymmdd'])
	
def libArteSearch():
	search_string = libMediathek.getSearchString()
	return libArteJsonParser.getSearch(search_string)

def libArteListSearch(searchString=False):
	if not searchString:
		searchString = params['searchString']
	return search(searchString)
		
def libArtePlay():
	return libArteJsonParser.getVideoUrlWeb(params['url'],params['title'],params['plot'],params['thumb'],params['duration'])
	
def headUrl(url):#TODO: move to libmediathek3
	libMediathek.log(url)
	import urllib2
	req = urllib2.Request(url)
	req.get_method = lambda : 'HEAD'
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0')
	
	response = urllib2.urlopen(req)
	info = response.info()
	response.close()
	return info

def libArteSelectLang():
	return libArteJsonParser.selectLang(params['url'])
	
def list():	
	modes = {
	'libArteListMain': libArteListMain,
	'libArteListShows': libArteListShows,
	'libArteThemes': libArteThemes,
	'libArteListVideos': libArteListVideos,
	'libArteListDate': libArteListDate,
	'libArteListDateVideos': libArteListDateVideos,
	'libArteSearch': libArteSearch,
	'libArteListSearch': libArteListSearch,
	'libArtePlay': libArtePlay,
	'libArteSelectLang': libArteSelectLang
	}
	
	global params
	params = libMediathek.get_params()
	global pluginhandle
	pluginhandle = int(sys.argv[1])
	mode = params.get('mode','libArteListMain')
	if mode == 'libArtePlay':
		libMediathek.play(libArtePlay())
	else:
		l = modes.get(mode)()
		libMediathek.addEntries(l)
		libMediathek.endOfDirectory()	
