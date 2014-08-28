//////

bind 

/////

The bind  will create a socket and listen for a connection and launch cmd.exe piped via the socket. Simply run it .\bind.ps1 to execute.

///////

powerdump.ps1

//////

Just run powerdump.ps1 and type "DumpHashes" in order to dump the SAM
database from the system.

//////

Createcmd.ps1

///////

If you want to bypass execution restriction policies, simply take your
code that you want to get passed and execute the createcmd.ps1 with the
following syntax:

.\createcmd.ps1 psfiletogetencoded.ps1 | Out-File mycmd.bat ascii

This will create a .bat file that will drop you into a powershell
environment with your variables pre-loaded