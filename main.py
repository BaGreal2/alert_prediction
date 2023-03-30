import subprocess

# This is our shell command, executed by Popen.

b = subprocess.Popen("scrapy crawl alerts -o alerts.json", stdout=subprocess.PIPE, shell=True)
a = subprocess.Popen("python3 src/generate_prob/generate.py", stdout=subprocess.PIPE, shell=True)
p = subprocess.Popen("python3 src/bot/bot.py", stdout=subprocess.PIPE, shell=True)

print(b.communicate())
print(a.communicate())
print(p.communicate())
