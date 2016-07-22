#!/usr/bin/env python
##
##
# Script to check if a http/https url works. 
# privide the url as first arg
# Long as we get a reponse code, regarlesss of the status, its deemed success. i.e we can connect to the endpoint.
# I used this script to verify various vpn connectivity after network team done firewall rules.
# Abdul Karim 
# 22/07/2016 
#
# exmaple
# python urltest.py https://www.google.com
#
# add multiple lines in a file
# cat urls.txt
# https://www.google.com
# http://www.bbc.co.uk
# 
# run in for loop:
# for url in $(cat urls.txt ); do python urltest.py $url; done

import urllib2
import sys, base64,getpass


def internet_on(thisurl):
    try:
        response=urllib2.urlopen(thisurl,timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def getPage(theurl):
	# usenrma/password not really needed for this test, so set it to anything
	#username = raw_input("Enter username :")
	#password = getpass.getpass("Enter your password for user ["+username+"] :")
	username='vpntest'
	password='vpntest'
	req = urllib2.Request(theurl)
	try:
		handle = urllib2.urlopen(req,timeout=2)
	except IOError, e:
	    # here we *want* to fail
	    pass
	else:
		return True

	base64string = base64.encodestring(
                '%s:%s' % (username, password))[:-1]
	authheader =  "Basic %s" % base64string
	req.add_header("Authorization", authheader)
	try:
		handle = urllib2.urlopen(req,timeout=1)
	except urllib2.HTTPError, err:
	    # here we shouldn't fail if the username/password is right
	    if ( str(err.code) == "404" or str(err.code) == "403" ):
	    	#print "Url / user  not found : " + str(err.code) 
		return True
	    else:
	    	#print "It looks like the username or password is wrong. "  +str (err.code)
		return True
	#except urllib2.URLError, uerr:
	#	print uerr
	#	return True
	except IOError, e:
	  # if get cert warning, normal on selfsigned cets, we don't care.  its means connection worked, so success. we are not worried about ssl warning here.
	  if 'CERTIFICATE_VERIFY_FAILED' in  str(e.reason):
		return True
	  return False
	thepage = handle.read()
	return json.loads(thepage)

if len(sys.argv) != 2:
	print "Usage: $0 http://url_to_test"
	sys.exit(1)
url=sys.argv[1]
if getPage(url):
	print url,",Success"
else:
	print url,",Fail"
