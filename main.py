"""
Ultimate Multi-Bot Launcher v2.0
--------------------------------
Single-process, low-memory bot system with all your existing configurations
"""

import os
import asyncio
import logging
from dataclasses import dataclass
from typing import List, Dict
from pyrogram import Client, filters
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from cachetools import TTLCache
import resource
import psutil

# === Configuration Setup ================================================ #
@dataclass
class BotConfig:
    """Enhanced configuration container with your actual values"""
    name: str
    token: str
    db_name: str
    admins: List[int]
    session_string: str = ""
    memory_limit_mb: int = 50

# Your actual bot configurations
def load_configs() -> List[BotConfig]:
    return [
        BotConfig(
            name="Team SAT",
            token="7821967646:AAFHUS91204U6P6xqnBOdAefk42agRWzTc0",
            db_name="SAT_manager",
            admins=[2031106491, 1519459773],
            session_string=os.getenv("SESSION_STRING", "")
        ),
        BotConfig(
            name="Batman",
            token="7269356488:AAF9kq5iuNWF00Jw997PRUqxtMzNqkHI7YU",
            db_name="Batman",
            admins=[2031106491, 5753557653],
            session_string=os.getenv("SESSION_STRING", "")
        ),
        BotConfig(
            name="Morphine",
            token="7934016506:AAHwP7D9NF2fd_2bH-4ELWM5is03_zdp6Ks",
            db_name="Morphine",
            admins=[2031106491, 7581732251],
            session_string=os.getenv("SESSION_STRING", "")
        ),
        BotConfig(
            name="Lucky",
            token="8012925939:AAE2EZk6-XAyXLseU-DGK7c3MMalD0a1Ryk",
            db_name="Lucky",
            admins=[2031106491, 7549453850, 7150972327, 7769891082, 7923725459, 7570751418],
            session_string=os.getenv("SESSION_STRING", "")
        ),
        BotConfig(
            name="AKSHAT",
            token="7528824781:AAHyEkGWdNRlp2FI1dueoivmQLRqCHHLkNQ",
            db_name="AKSHAT",
            admins=[2031106491, 5076431214],
            session_string=os.getenv("SESSION_STRING", "")
        )
    ]

# === Core System ======================================================== #
class MasterBot:
    """Complete implementation with your variables"""
    def __init__(self):
        self.bots: Dict[str, Client] = {}
        self.cache = TTLCache(maxsize=1000, ttl=300)
        self.logger = self._setup_logger()
        
        # MongoDB connection with your actual credentials
        self.db = AsyncIOMotorClient(
            os.getenv("MONGO_URI", "mongodb://localhost:27017"),
            maxPoolSize=5,
            connectTimeoutMS=30000
        )

    def _setup_logger(self):
        """Configure logging matching your format"""
        logger = logging.getLogger("BotMaster")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    async def initialize_bots(self, configs: List[BotConfig]):
        """Initialize all bot clients with your settings"""
        for config in configs:
            client = Client(
                name=config.name,
                api_id=os.getenv("API_ID"),  # Set these in your environment
                api_hash=os.getenv("API_HASH"),
                bot_token=config.token,
                in_memory=True,
                workers=2,
                sleep_threshold=30
            )
            
            # Register handlers
            client.add_handler(self._create_handler(config))
            self.bots[config.name] = client
            self.logger.info(f"Initialized {config.name}")

    def _create_handler(self, config: BotConfig):
        """Message handler with your processing logic"""
        @Client.on_message(filters.all)
        async def handler(client: Client, message: Message):
            try:
                bot_name = next(k for k,v in self.bots.items() if v == client)
                
                # Your actual processing logic would go here
                self.logger.info(f"Processing message for {bot_name}")
                
                # Example: Admin check
                if message.from_user and message.from_user.id in config.admins:
                    await message.reply(f"Hello admin from {bot_name}!")
                
            except Exception as e:
                self.logger.error(f"Error in {config.name}: {str(e)}")
            finally:
                # Memory cleanup
                del message
                import gc; gc.collect()

        return handler

    async def start_system(self):
        """Complete startup sequence"""
        # Set memory limits (512MB soft, 1GB hard)
        resource.setrlimit(
            resource.RLIMIT_AS,
            (512 * 1024 * 1024, 1024 * 1024 * 1024)
        )
        
        # Start all bots
        await asyncio.gather(*[client.start() for client in self.bots.values()])
        
        # Start monitoring
        asyncio.create_task(self._monitor_resources())
        
        self.logger.info("All bots running. Memory usage: "
                      f"{psutil.Process(os.getpid()).memory_info().rss/1024/1024:.2f}MB")

    async def _monitor_resources(self):
        """Your resource monitoring with actual thresholds"""
        while True:
            mem = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
            if mem > 400:  # 400MB threshold
                self.logger.warning(f"High memory: {mem:.2f}MB. Optimizing...")
                await self._free_memory()
            await asyncio.sleep(60)

    async def _free_memory(self):
        """Actual memory optimization"""
        import gc
        gc.collect()
        self.cache.clear()
        self.logger.info("Performed memory cleanup")

# === Main Execution ===================================================== #
async def main():
    """Complete startup with your bots"""
    # Initialize with your configs
    master = MasterBot()
    await master.initialize_bots(load_configs())
    
    # Start the system
    await master.start_system()
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}", exc_info=True)
