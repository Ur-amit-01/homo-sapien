
"""
Multi-Bot Launcher
------------------
Main launcher script using external logging configuration
"""

import subprocess
import os
import re
from multiprocessing import Process
from logging import setup_logger, get_logger

# Base configuration
BASE_DIR = "/app"
REPO_URL = "https://github.com/Ur-amit-01/Post-Manager.git"
ID_PATTERN = re.compile(r'^\d{5,}$')

# Initialize main logger
logger = setup_logger('BotLauncher')


# ====================== BOT CONFIGS ====================== #
BOT1_CONFIG = {
    "name": "Team SAT",
    "token": "7408...",
    "db_name": "T1",
    "admins": "7150972327"
}

BOT2_CONFIG = {
    "name": "Batman",
    "token": "8113...",
    "db_name": "T2",
    "admins": "7150972327 1234567890"
}

BOT3_CONFIG = {
    "name": "Harshal",
    "token": "7334882078:AAHrEbyz8YW-__QCGz8Om2JrNdvxW3NPhXE",
    "db_name": "Harshal",
    "admins": "7150972327 1084487776"
}

ACTIVE_BOTS = [BOT1_CONFIG, BOT2_CONFIG, BOT3_CONFIG]


# ====================== CORE FUNCTION ====================== #

def install_requirements():
    """Install required packages for all bots"""
    logger.info("Installing requirements...")
    temp_dir = os.path.join(BASE_DIR, "temp-install")
    try:
        os.chdir(BASE_DIR)
        subprocess.run(["git", "clone", REPO_URL, temp_dir], check=True)
        os.chdir(temp_dir)
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        logger.info("Requirements installed successfully")
    except Exception as e:
        logger.error(f"Failed to install requirements: {str(e)}")
        raise
    finally:
        os.chdir(BASE_DIR)
        subprocess.run(["rm", "-rf", temp_dir], check=True)

def setup_admin_variable(admin_ids):
    """Process admin IDs and set environment variable"""
    try:
        admin_list = [int(admin) if ID_PATTERN.search(admin) else admin 
                     for admin in admin_ids.split()]
        os.environ["ADMIN"] = " ".join(str(admin) for admin in admin_list)
        get_logger('AdminSetup').info(f"Admin IDs processed: {admin_list}")
        return admin_list
    except Exception as e:
        get_logger('AdminSetup').error(f"Error processing admin IDs: {str(e)}")
        raise

def launch_bot(bot_config):
    """Launch a single bot instance"""
    bot_logger = get_logger(f"Bot.{bot_config['name']}")
    bot_logger.info("Starting bot instance")
    
    bot_dir = os.path.join(BASE_DIR, bot_config["name"])
    
    try:
        # Setup bot directory
        os.chdir(BASE_DIR)
        subprocess.run(["git", "clone", REPO_URL, bot_dir], check=True)
        os.chdir(bot_dir)
        
        # Configure environment
        os.environ["BOT_TOKEN"] = bot_config["token"]
        os.environ["DB_NAME"] = bot_config["db_name"]
        
        # Setup admin variables
        admin_list = setup_admin_variable(bot_config["admins"])
        bot_logger.info(f"Configured admins: {admin_list}")
        
        # Launch bot
        bot_logger.info("Launching bot process")
        subprocess.run(["python", "bot.py"], check=True)
    except Exception as e:
        bot_logger.error(f"Bot failed: {str(e)}")
        raise

# ====================== MAIN ====================== #
def main():
    """Main execution function"""
    logger.info("="*50)
    logger.info(" MULTI-BOT LAUNCHER ".center(50, "="))
    logger.info("="*50)
    
    try:
        install_requirements()
        
        processes = []
        for bot_config in ACTIVE_BOTS:
            p = Process(target=launch_bot, args=(bot_config,))
            p.start()
            processes.append(p)
            logger.info(f"Started process for {bot_config['name']}")
        
        for p in processes:
            p.join()
            
        logger.info("All bot processes completed")
    except Exception as e:
        logger.critical(f"Launcher failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
