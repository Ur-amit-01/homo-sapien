import subprocess
import os
from multiprocessing import Process

def run_bot1():
    subprocess.call(["git", "clone", "https://github.com/user/bot1.git"])
    os.chdir("bot1")
    subprocess.call(["pip", "install", "-r", "requirements.txt"])
    subprocess.call(["python", "main.py"])

def run_bot2():
    subprocess.call(["git", "clone", "https://github.com/user/bot2.git"])
    os.chdir("../")  # Back to parent before cloning
    subprocess.call(["git", "clone", "https://github.com/user/bot2.git"])
    os.chdir("bot2")
    subprocess.call(["pip", "install", "-r", "requirements.txt"])
    subprocess.call(["python", "main.py"])

if __name__ == "__main__":
    p1 = Process(target=run_bot1)
    p2 = Process(target=run_bot2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
