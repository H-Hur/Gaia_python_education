#ASYNCHRONOUS REQUEST Example from Gaia website

#Python 3
import http.client as httplib
import urllib.parse as urllib
import time
from xml.dom.minidom import parseString

host = "gea.esac.esa.int"
port = 443
pathinfo = "/tap-server/tap/async"

# Equtorial Coordinates in HMS, DMS
ra1 = 8    # hour
ra2 = 51   # arcmin
ra3 = 23   # arcsec
dec1 = 11  # degree
dec2 = 48   # minute
dec3 = 5   # second

# Set output csv file name 
output = "M67_gaia_dr3.csv"

# cal RA, DEC in degree
ra = 15*(ra1 + ra2/60 + ra3/3600)
dec = dec1 + dec2/60 + dec3/3600
if dec < 0: dec = dec1 - dec2/60 - dec3/3600
fov = 0.5 # in degree

print(ra,dec,fov)
print(str(ra),str(dec),str(fov))
#-------------------------------------
#Create job

params = urllib.urlencode({\
	"REQUEST": "doQuery", \
	"LANG":    "ADQL", \
	"FORMAT":  "csv", \
	"PHASE":  "RUN", \
	"JOBNAME":  "Any name (optional)", \
	"JOBDESCRIPTION":  "Any description (optional)", \
	"QUERY":   "SELECT DISTANCE(POINT("+str(ra)+", "+str(dec)+"),POINT(ra,dec)) AS dist, * FROM gaiadr3.gaia_source  WHERE 1=CONTAINS(POINT("+str(ra)+", "+str(dec)+"),CIRCLE(ra,dec, "+str(fov)+")) ORDER BY dist ASC"
	})

headers = {\
	"Content-type": "application/x-www-form-urlencoded", \
	"Accept":       "text/plain" \
	}

connection = httplib.HTTPSConnection(host, port)
connection.request("POST",pathinfo,params,headers)

#Status
response = connection.getresponse()
print ("Status: " +str(response.status), "Reason: " + str(response.reason))

#Server job location (URL)
location = response.getheader("location")
print ("Location: " + location)

#Jobid
jobid = location[location.rfind('/')+1:]
print ("Job id: " + jobid)

connection.close()

#-------------------------------------
#Check job status, wait until finished

while True:
	connection = httplib.HTTPSConnection(host, port)
	connection.request("GET",pathinfo+"/"+jobid)
	response = connection.getresponse()
	data = response.read()
	#XML response: parse it to obtain the current status
	#(you may use pathinfo/jobid/phase entry point to avoid XML parsing)
	dom = parseString(data)
	phaseElement = dom.getElementsByTagName('uws:phase')[0]
	phaseValueElement = phaseElement.firstChild
	phase = phaseValueElement.toxml()
	print ("Status: " + phase)
	#Check finished
	if phase == 'COMPLETED': break
	#wait and repeat
	time.sleep(0.2)

connection.close()

#-------------------------------------
#Get results
connection = httplib.HTTPSConnection(host, port)
connection.request("GET",pathinfo+"/"+jobid+"/results/result")
response = connection.getresponse()
data = response.read().decode('iso-8859-1')
#print(type(data))
#print(data)
outputFile = open(output, "w",encoding='UTF-8')
outputFile.write(data)
outputFile.close()
connection.close()
#import urllib
print ("Data saved in: " + output)
