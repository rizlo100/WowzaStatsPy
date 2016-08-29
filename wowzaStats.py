#!/usr/bin/python

#
# A python script to parse the XML Output from the Wowza connectioncounts
# http conenctor and print the info
#
#
# Usage: ./wowzaStats.py HOST USER PASS
#
#

import sys
import urllib2
import commands

from xml.dom.minidom import parseString

#Load the XML from Wowza host.
def loadxml(host, username, password):
#    url = 'http://' + host + ':8086/connectioncounts'
    url = 'http://' + host + ':1935/connectioncounts'
    mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    mgr.add_password(None,url,username,password)

    opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(mgr), urllib2.HTTPDigestAuthHandler(mgr))

    urllib2.install_opener(opener)

    try:
        f = urllib2.urlopen(url)
        return f.read()
    except:
                return ''

#Set default variables.
_host = ''
_username = ''
_password = ''

#Set variables through command line arguments.
if len(sys.argv) > 1:
    _host = sys.argv[1]
if len(sys.argv) > 2:
    _username = sys.argv[2]
if len(sys.argv) > 3:
    _password = sys.argv[3]

_xml = loadxml(_host, _username, _password)

dom = parseString(_xml)



## Get Global Connections
GlobalConnCur = dom.getElementsByTagName('ConnectionsCurrent')
GlobalConnAccepted = dom.getElementsByTagName('ConnectionsTotalAccepted')
GlobalConnRejected = dom.getElementsByTagName('ConnectionsTotalRejected')
GlobalInBytes = dom.getElementsByTagName('MessagesInBytesRate')
GlobalOutBytes = dom.getElementsByTagName('MessagesOutBytesRate')


print "Global Wowza Current Active Connections: " + GlobalConnCur[0].firstChild.nodeValue
print "Global Wowza Accepted Connections: " + GlobalConnAccepted[0].firstChild.nodeValue
print "Global Wowza Rejected Connections: " + GlobalConnRejected[0].firstChild.nodeValue
print "Global Wowza IN Bytes/s: " + GlobalInBytes[0].firstChild.nodeValue
print "Global Wowza OUT Bytes/s: " + GlobalOutBytes[0].firstChild.nodeValue

# Loop through the stream applications and print stream info 

applications = dom.getElementsByTagName('Application')

for apps in applications:
	AppName = apps.getElementsByTagName('Name')
	ConnConnect = apps.getElementsByTagName('ConnectionsCurrent')
	AcceptConnect = apps.getElementsByTagName('ConnectionsTotalAccepted')
	print
	print "Application: "
	print AppName[0].firstChild.nodeValue + " - Connected Clients: " + ConnConnect[0].firstChild.nodeValue
	print "Active Streams:"
	print
	
	streams = apps.getElementsByTagName('Stream')
	for stream in streams:
		StreamName = stream.getElementsByTagName('Name')
		StreamConn = stream.getElementsByTagName('SessionsTotal')
		Flash = stream.getElementsByTagName('SessionsFlash')
		Cup = stream.getElementsByTagName('SessionsCupertino')
		San = stream.getElementsByTagName('SessionsSanJose')
		Smooth = stream.getElementsByTagName('SessionsSmooth')
		Rtsp = stream.getElementsByTagName('SessionsRTSP')
		Dash = stream.getElementsByTagName('SessionsMPEGDash')

		print StreamName[0].firstChild.nodeValue
		print "Has " + StreamConn[0].firstChild.nodeValue + " clients watching. Flash:" + Flash[0].firstChild.nodeValue + \
		" HLS:" + Cup[0].firstChild.nodeValue + " HDS:" + San[0].firstChild.nodeValue + " Smooth:" + \
		Smooth[0].firstChild.nodeValue + " RTSP:" + Rtsp[0].firstChild.nodeValue + " Dash:" + \
		Dash[0].firstChild.nodeValue
		print

