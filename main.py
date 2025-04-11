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
    "token": "7821967646:AAFHUS91204U6P6xqnBOdAefk42agRWzTc0",
    "db_name": "SAT_manager",
    "admins": "7150972327 2031106491 1519459773",
    "session_string": "BQFP49AAROLIHpH9tfjlrEewakOd-NndU3oDb9F1OJMp3cLaksypCJuuS1Qm8Bz6FjsIXzlyq1C2_Tz4gKj6vz2vZ-bElYZ8-0NLco6I74pWQOi2GQqBfvX9ls8EC3coHPY6YzfkEORGOt-i_Y05fw_UXE1NubilnLt1AOPA25gueZX-j8Jdf4c-gsA4i2qdaVjaWSNMba7F-aZ7W3KEFl3CO0KaVRqwFT9lDXEcZVc_UuYr0FG0f9qOmh7vyo-M7fr6lX7RzJjxR7AONx_9QB9rHWL3cogjbdhR9wGUoT2n7xbMKSJbtZH4L7W8H3NtaUl-svjOTmnHqQ4i11H3gsUMCbxR0QAAAAGVhUI_AA"  # Add session string if needed
}

BOT2_CONFIG = {
    "name": "Batman",
    "token": "7269356488:AAF9kq5iuNWF00Jw997PRUqxtMzNqkHI7YU",
    "db_name": "Batman",
    "admins": "7150972327 5753557653 2031106491 1519459773",
    "session_string": "BQFP49AAROLIHpH9tfjlrEewakOd-NndU3oDb9F1OJMp3cLaksypCJuuS1Qm8Bz6FjsIXzlyq1C2_Tz4gKj6vz2vZ-bElYZ8-0NLco6I74pWQOi2GQqBfvX9ls8EC3coHPY6YzfkEORGOt-i_Y05fw_UXE1NubilnLt1AOPA25gueZX-j8Jdf4c-gsA4i2qdaVjaWSNMba7F-aZ7W3KEFl3CO0KaVRqwFT9lDXEcZVc_UuYr0FG0f9qOmh7vyo-M7fr6lX7RzJjxR7AONx_9QB9rHWL3cogjbdhR9wGUoT2n7xbMKSJbtZH4L7W8H3NtaUl-svjOTmnHqQ4i11H3gsUMCbxR0QAAAAGVhUI_AA"
}

BOT3_CONFIG = {
    "name": "Harshal",
    "token": "7334882078:AAHrEbyz8YW-__QCGz8Om2JrNdvxW3NPhXE",
    "db_name": "Harshal",
    "admins": "7150972327 1084487776",
    "session_string": os.environ.get("HARSHAL_SESSION_STRING", "BQFP49AAROLIHpH9tfjlrEewakOd-NndU3oDb9F1OJMp3cLaksypCJuuS1Qm8Bz6FjsIXzlyq1C2_Tz4gKj6vz2vZ-bElYZ8-0NLco6I74pWQOi2GQqBfvX9ls8EC3coHPY6YzfkEORGOt-i_Y05fw_UXE1NubilnLt1AOPA25gueZX-j8Jdf4c-gsA4i2qdaVjaWSNMba7F-aZ7W3KEFl3CO0KaVRqwFT9lDXEcZVc_UuYr0FG0f9qOmh7vyo-M7fr6lX7RzJjxR7AONx_9QB9rHWL3cogjbdhR9wGUoT2n7xbMKSJbtZH4L7W8H3NtaUl-svjOTmnHqQ4i11H3gsUMCbxR0QAAAAGVhUI_AA")  # Example of getting from env
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
