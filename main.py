import subprocess
import os
from multiprocessing import Process

# Install requirements once
def install_requirements():
    os.chdir("/app")
    subprocess.call(["git", "clone", "https://github.com/Ur-amit-01/Post-Manager.git", "temp-install"])
    os.chdir("temp-install")
    subprocess.call(["pip", "install", "-r", "requirements.txt"])
    os.chdir("/app")
    subprocess.call(["rm", "-rf", "temp-install"] 
    

def run_bot1():
    os.chdir("/app")
    subprocess.call(["git", "clone", "https://github.com/Ur-amit-01/Post-Manager.git", "Post-Manager-Bot1"])
    os.chdir("Post-Manager-Bot1")
    
    # Set environment variables for bot 1
    os.environ["BOT_TOKEN"] = "7408399689:AAGyXnXAIeja9qyg7eEPghKkmL4Z4OJy5-w"
    os.environ["DB_NAME"] = "T1"
    
    subprocess.call(["pip", "install", "-r", "requirements.txt"])
    subprocess.call(["python", "bot.py"])

def run_bot2():
    os.chdir("/app")
    subprocess.call(["git", "clone", "https://github.com/Ur-amit-01/Post-Manager.git", "Post-Manager-Bot2"])
    os.chdir("Post-Manager-Bot2")

    # Set environment variables for bot 2
    os.environ["BOT_TOKEN"] = "8113183687:AAG4EYlhk5jlSgHCobLIqjsKW_lUIseKVMs"
    os.environ["DB_NAME"] = "T2"
    
    subprocess.call(["pip", "install", "-r", "requirements.txt"])
    subprocess.call(["python", "bot.py"])

def run_bot3():
    os.chdir("/app")
    subprocess.call(["git", "clone", "https://github.com/Ur-amit-01/Post-Manager.git", "Post-Manager-Bot3"])
    os.chdir("Post-Manager-Bot3")

    # Set environment variables for bot 3
    os.environ["BOT_TOKEN"] = "7557297602:AAH6-43MKGE0umypUgeonsfk41wOrsDKCnM"
    os.environ["DB_NAME"] = "T3"
    
    subprocess.call(["pip", "install", "-r", "requirements.txt"])
    subprocess.call(["python", "bot.py"])
    
if __name__ == "__main__":
    install_requirements()
    p1 = Process(target=run_bot1)
    p2 = Process(target=run_bot2)
    p3 = Process(target=run_bot3)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
