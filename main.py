"""
Multi-Bot Launcher
------------------
Main launcher script using external logging configuration
"""

import subprocess
import os
import re
from multiprocessing import Process
from logger_setup import *
# Base configuration
BASE_DIR = "/app"
ID_PATTERN = re.compile(r'^\d{5,}$')

# Initialize main logger
logger = setup_logger('BotLauncher')
SESSION_STRING = "BQFP49AAiVku9pI3VZylmYZ-LJi7gUSLC7iM873LFaQtV7ozu83PEvi3N6ypHhtLaSfTDW9CC7YMK5W6jwgFuJ0ThauW7GnSgkDR7ERtmJtGptXcgA0SX3eWvRepBMWfD3jhGTOK5CveP7UYp5JHsMDMeBAkmwic0R9YWXkwU8jl-bOO8pWisoZkjqOX2-kVacxifW9ZRe52O8zmNB3dF_VTcRCGvp58ZfzaJLHT5lE4_T_TVuHqZK9YUzzstNAHN7yDVZZc49kpRTaGeMhCxjCuSyGDO7iP0NCqzd-DJDr3qe7DT-WfhfqgNMjqoC1BjB5Ksm7qxGK10rPzfqU6vz_5bZSEnQAAAAGVhUI_AA"

# ====================== BOT CONFIGS ====================== #
BOT1_CONFIG = {
    "name": "Team SAT",
    "token": "7821967646:AAFHUS91204U6P6xqnBOdAefk42agRWzTc0",
    "db_name": "SAT_manager",
    "admins": "7150972327 2031106491 1519459773 6803505727",
    "session_string": SESSION_STRING
}

BOT2_CONFIG = {
    "name": "Batman",
    "token": "7269356488:AAF9kq5iuNWF00Jw997PRUqxtMzNqkHI7YU",
    "db_name": "Batman",
    "admins": "5753557653",
    "session_string": SESSION_STRING
}

BOT3_CONFIG = {
    "name": "Harshal",
    "token": "7334882078:AAHrEbyz8YW-__QCGz8Om2JrNdvxW3NPhXE",
    "db_name": "Harshal",
    "admins": "7150972327 1084487776",
    "session_string": SESSION_STRING
}

BOT4_CONFIG = {
    "name": "Lucky",
    "token": "8012925939:AAE2EZk6-XAyXLseU-DGK7c3MMalD0a1Ryk",
    "db_name": "Lucky",
    "admins": "7549453850 7150972327 7769891082 7923725459 2031106491 7570751418",
    "session_string": SESSION_STRING
}

BOT5_CONFIG = {
    "name": "AKSHAT",
    "token": "7528824781:AAHyEkGWdNRlp2FI1dueoivmQLRqCHHLkNQ",
    "db_name": "AKSHAT",
    "admins": "2031106491 5076431214",
    "session_string": SESSION_STRING
}
ACTIVE_BOTS = [BOT1_CONFIG, BOT2_CONFIG, BOT3_CONFIG, BOT4_CONFIG, BOT5_CONFIG]


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

def setup_environment_vars(bot_config):
    """Setup all environment variables for the bot"""
    try:
        # Process admin IDs
        admin_list = [int(admin) if ID_PATTERN.search(admin) else admin 
                    for admin in bot_config["admins"].split()]
        os.environ["ADMIN"] = " ".join(str(admin) for admin in admin_list)
        
        # Set other environment variables
        os.environ["BOT_TOKEN"] = bot_config["token"]
        os.environ["DB_NAME"] = bot_config["db_name"]
        os.environ["SESSION_STRING"] = bot_config.get("session_string", "")
        
        get_logger('EnvSetup').info(
            f"Environment configured for {bot_config['name']}\n"
            f"Admins: {admin_list}\n"
            f"DB: {bot_config['db_name']}\n"
            f"Session: {'set' if bot_config.get('session_string') else 'not set'}"
        )
        return admin_list
    except Exception as e:
        get_logger('EnvSetup').error(f"Error setting up environment: {str(e)}")
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
        setup_environment_vars(bot_config)
        
        # Launch bot
        bot_logger.info("Launching bot process")
        subprocess.run(["python", "bot.py"], check=True)
    except Exception as e:
        bot_logger.error(f"Bot failed: {str(e)}")
        raise
    finally:
        # Clean up environment variables
        for var in ["ADMIN", "BOT_TOKEN", "DB_NAME", "SESSION_STRING"]:
            if var in os.environ:
                del os.environ[var]

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
