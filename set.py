import sys
import os
import time

os.system("pkill python")
command = "python /var/www/html/redding/main.py " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + sys.argv[4]
print command
time.sleep(0.1)
os.system(command)
