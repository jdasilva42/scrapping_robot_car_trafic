from asyncio.log import logger
from Robot import *
from datetime import datetime
import logging

LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(
    filename='log_robot_nantes.log',
    level=logging.INFO,
    format = LOG_FORMAT,
    #filemode='w'
)

logger = logging.getLogger()

url='https://nantesmetropole.opendatasoft.com/explore/dataset/244400404_fluidite-axes-routiers-nantes-metropole/export/'
PATH = '/app'

robot = Robot(PATH,url)
logger.info('Le robot a rempli sa tâche')

    
