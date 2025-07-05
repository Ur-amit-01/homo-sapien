"""
Optimized Multi-Bot Launcher
---------------------------
Memory-efficient launcher that shares codebase across all bots
"""

import subprocess
import os
import re
import sys
from multiprocessing import Process
from logger_setup import *
from collections import namedtuple

# Base configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHARED_CODE_DIR = os.path.join(BASE_DIR, "shared_bot_code")
ID_PATTERN = re.compile(r'^\d{5,}$')

# Define BotConfig structure
BotConfig = namedtuple('BotConfig', ['name', 'token', 'db_name', 'admins', 'session_string'])

# ====================== BOT CONFIGS ====================== #
BOT_CONFIGS = [
    BotConfig(
        name="A",
        token="6920460183:AAHKos4mftdTZDu19RE-41Tfhvhck-F6H2c",
        db_name="A",
        admins=[2031106491, 1519459773],
        session_string=os.getenv("SESSION_STRING", "")
    ),
    BotConfig(
        name="B",
        token="6602223723:AAEfW7bAtToE_E9jOV1690c4-sOLQO5gxA8",
        db_name="B",
        admins=[2031106491, 5753557653],
        session_string=os.getenv("SESSION_STRING", "")
    ),
    BotConfig(
        name="C",
        token="7805843798:AAFVUpjYdZOr2bND92ubxjqh2b_M4kSZkoo",
        db_name="C",
        admins=[2031106491, 7581732251],
        session_string=os.getenv("SESSION_STRING", "")
    ),
    BotConfig(
        name="D",
        token="8075405859:AAH-vh6v3dnoaCGGQe7cD2XQi5F9HdXw1Nk",
        db_name="D",
        admins=[2031106491, 7549453850, 7150972327, 7769891082, 7923725459, 7570751418],
        session_string=os.getenv("SESSION_STRING", "")
    ),
    BotConfig(
        name="E",
        token="7816211165:AAFqKE8p6-l8DNxJvLZeX4UO3eRQEYcN_Ho",
        db_name="E",
        admins=[2031106491, 5076431214],
        session_string=os.getenv("SESSION_STRING", "")
    )
]

# Initialize main logger
logger = setup_logger('BotLauncher')

# ====================== CORE FUNCTIONS ====================== #

def setup_shared_code():
    """Set up a single shared code directory for all bots"""
    if os.path.exists(SHARED_CODE_DIR):
        logger.info("Shared code directory already exists, updating...")
        try:
            os.chdir(SHARED_CODE_DIR)
            subprocess.run(["git", "pull"], check=True)
            os.chdir(BASE_DIR)
        except subprocess.CalledProcessError:
            logger.warning("Failed to update, using existing code")
    else:
        logger.info("Cloning shared code repository...")
        try:
            subprocess.run(["git", "clone", REPO_URL, SHARED_CODE_DIR], check=True)
            # Install requirements once for all bots
            os.chdir(SHARED_CODE_DIR)
            subprocess.run(["pip", "install", "--quiet", "-r", "requirements.txt"], check=True)
            os.chdir(BASE_DIR)
            logger.info("Shared code setup complete")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone repository: {e}")
            sys.exit(1)

def prepare_bot_environment(bot_config):
    """Prepare environment variables for a bot"""
    env = os.environ.copy()
    
    # Process admin IDs
    admin_list = [str(admin) for admin in bot_config.admins]
    env["ADMIN"] = " ".join(admin_list)
    
    # Set other environment variables
    env["BOT_TOKEN"] = bot_config.token
    env["DB_NAME"] = bot_config.db_name
    env["SESSION_STRING"] = bot_config.session_string
    
    get_logger('EnvSetup').info(
        f"Prepared environment for {bot_config.name}\n"
        f"Admins: {admin_list}\n"
        f"DB: {bot_config.db_name}"
    )
    
    return env

def run_bot_instance(bot_config):
    """Run a single bot instance with its own environment"""
    bot_logger = get_logger(f"Bot.{bot_config.name}")
    bot_logger.info("Starting bot process")
    
    try:
        # Prepare environment
        env = prepare_bot_environment(bot_config)
        
        # Launch bot in the shared code directory
        os.chdir(SHARED_CODE_DIR)
        subprocess.run(
            [sys.executable, "bot.py"],
            env=env,
            check=True
        )
    except Exception as e:
        bot_logger.error(f"Bot process failed: {str(e)}")
    finally:
        os.chdir(BASE_DIR)
        bot_logger.info("Bot process terminated")

# ====================== MAIN ====================== #
def main():
    """Main execution function"""
    logger.info("="*50)
    logger.info(" OPTIMIZED BOT LAUNCHER ".center(50, "="))
    logger.info("="*50)
    
    try:
        # Set up shared code once
        setup_shared_code()
        
        # Launch bots
        processes = []
        for config in BOT_CONFIGS:
            p = Process(target=run_bot_instance, args=(config,))
            p.start()
            processes.append(p)
            logger.info(f"Started {config.name} (PID: {p.pid})")
        
        # Monitor processes
        while processes:
            for p in processes[:]:
                if not p.is_alive():
                    config = BOT_CONFIGS[processes.index(p)]
                    logger.warning(f"Process {p.pid} ({config.name}) terminated")
                    processes.remove(p)
            
            if processes:
                # Check every 5 seconds
                for p in processes:
                    p.join(timeout=5)
        
        logger.info("All bot processes completed")
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.critical(f"Launcher failed: {str(e)}")
    finally:
        # Clean up
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join()

if __name__ == "__main__":
    main()
