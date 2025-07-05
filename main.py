"""
Fixed Multi-Bot Launcher v2.1
----------------------------
With guaranteed bot startup and message processing
"""

import os
import asyncio
import logging
from dataclasses import dataclass
from typing import List, Dict
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from cachetools import TTLCache
import resource
import psutil

# === Configuration Setup ================================================ #
@dataclass
class BotConfig:
    name: str
    token: str
    db_name: str
    admins: List[int]
    session_string: str = ""

def load_configs() -> List[BotConfig]:
    return [
        BotConfig(
            name="Team SAT",
            token="6920460183:AAHKos4mftdTZDu19RE-41Tfhvhck-F6H2c",
            db_name="A",
            admins=[2031106491, 1519459773],
            session_string=os.getenv("SESSION_STRING", "")
        ),
        BotConfig(
            name="B",
            token="6602223723:AAEfW7bAtToE_E9jOV1690c4-sOLQO5gxA8",
            db_name="Batman",
            admins=[2031106491, 5753557653],
            session_string=os.getenv("SESSION_STRING", "")
        ),
        BotConfig(
            name="C",
            token="7805843798:AAFVUpjYdZOr2bND92ubxjqh2b_M4kSZkoo",
            db_name="Morphine",
            admins=[2031106491, 7581732251],
            session_string=os.getenv("SESSION_STRING", "")
        ),
        BotConfig(
            name="D",
            token="8075405859:AAH-vh6v3dnoaCGGQe7cD2XQi5F9HdXw1Nk",
            db_name="Lucky",
            admins=[2031106491, 7549453850, 7150972327, 7769891082, 7923725459, 7570751418],
            session_string=os.getenv("SESSION_STRING", "")
        ),
        BotConfig(
            name="E",
            token="7816211165:AAFqKE8p6-l8DNxJvLZeX4UO3eRQEYcN_Ho",
            db_name="AKSHAT",
            admins=[2031106491, 5076431214],
            session_string=os.getenv("SESSION_STRING", "")
        )
    ]

# === Core System ======================================================== #
class MasterBot:
    def __init__(self):
        self.bots: Dict[str, Client] = {}
        self.cache = TTLCache(maxsize=1000, ttl=300)
        self.logger = self._setup_logger()
        self.db = AsyncIOMotorClient(
            os.getenv("MONGO_URI", "mongodb://localhost:27017"),
            maxPoolSize=5
        )

    def _setup_logger(self):
        logger = logging.getLogger("BotMaster")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    async def initialize_bots(self, configs: List[BotConfig]):
        """Initialize with proper startup sequence"""
        for config in configs:
            client = Client(
                name=config.name,
                api_id=os.getenv("API_ID"),
                api_hash=os.getenv("API_HASH"),
                bot_token=config.token,
                in_memory=True,
                workers=2
            )
            
            # Add handlers before starting
            client.add_handler(self._create_handler(config))
            self.bots[config.name] = client
            
            # Start each client immediately after initialization
            await client.start()
            self.logger.info(f"{config.name} started successfully. Bot ID: {client.me.id}")

    def _create_handler(self, config: BotConfig):
        @Client.on_message(filters.all)
        async def handler(client: Client, message: Message):
            try:
                bot_name = next(k for k,v in self.bots.items() if v == client)
                self.logger.info(f"New message for {bot_name}")
                
                # Your actual message processing here
                if message.from_user and message.from_user.id in config.admins:
                    await message.reply(f"{bot_name} is working!")
                    
            except Exception as e:
                self.logger.error(f"Error in {config.name}: {str(e)}")
            finally:
                del message
                import gc; gc.collect()

        return handler

    async def run(self):
        """Main execution with proper lifecycle"""
        resource.setrlimit(
            resource.RLIMIT_AS,
            (512 * 1024 * 1024, 1024 * 1024 * 1024)
        )
        
        configs = load_configs()
        await self.initialize_bots(configs)
        
        # Keep bots running
        self.logger.info("All bots active. Memory: "
                      f"{psutil.Process(os.getpid()).memory_info().rss/1024/1024:.2f}MB")
        
        # This keeps the event loop running
        await idle()

        # Cleanup on shutdown
        await self.stop()

    async def stop(self):
        """Proper shutdown"""
        for name, client in self.bots.items():
            if client.is_initialized:
                await client.stop()
                self.logger.info(f"Stopped {name}")

# === Main Execution ===================================================== #
async def main():
    master = MasterBot()
    try:
        await master.run()
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        await master.stop()

if __name__ == "__main__":
    asyncio.run(main())
