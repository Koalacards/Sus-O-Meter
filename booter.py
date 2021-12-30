import subprocess

while True:
    p = subprocess.Popen("python3 bot.py", shell=True).wait()

    if p!= 0:
        continue
    else:
        break