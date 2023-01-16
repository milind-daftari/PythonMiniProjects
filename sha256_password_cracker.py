from pwn import *
import sys

if len(sys.argv) != 2:
	print("Invalid arguments!")
	print("Usage: {} <sha256sum>". format(sys.argv[0]))
	exit()

input_hash = sys.argv[1]

wordlist_path = "/usr/share/wordlists/rockyou.txt"
attempts = 0

with log.progress("Attempting to crack {}!\n".format(input_hash)) as p:
	with open(wordlist_path, "r", encoding = 'latin-1') as wordlist:
		for word in wordlist:
			word = word.strip('\n').encode('latin-1')
			word_hash = sha256sumhex(word)
			p.status("[{}] {}".format(attempts, word.decode('latin-1'), word_hash))
			if word_hash == input_hash:
				p.success("Hash found after {} attempts!\n{} hashed to {}!".format(attempts, word.decode('latin-1'), word_hash))
				exit()
			attempts += 1
		p.failure("Hash not found!")
