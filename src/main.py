import os
import logger
import asyncio

from api.server import GeneratorRestAPI
from dotenv import load_dotenv

async def main():
    load_dotenv()
    logger.setup()
    
    if not os.path.isdir(os.getenv('IMAGES_PATH')):
        os.mkdir(os.getenv('IMAGES_PATH'))
    
    server = GeneratorRestAPI()
    server.start()
    
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()