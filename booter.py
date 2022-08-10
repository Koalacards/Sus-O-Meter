import asyncio
import subprocess
import tracemalloc

tracemalloc.start()

while True:
    p = subprocess.Popen("python3 bot.py", shell=True).wait()

    if p != 0:
        continue
    else:
        print("susometer stopped")
        snap = tracemalloc.take_snapshot()
        top_stats = snap.statistics("lineno")
        print(f"[Top 10]")
        for stat in top_stats[:10]:
            print(stat)
        asyncio.sleep(90)
