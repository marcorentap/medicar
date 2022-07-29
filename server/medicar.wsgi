import sys
import logging

logging.basicConfig(level=logging.DEBUG, filename='/var/www/medicar/server/medicar.log', format='%(asctime)s %(message)s')
sys.path.insert(0, '/var/www/medicar/server')
sys.path.insert(0, '/var/www/medicar/server/venv/lib/python3.8/site-packages')
from app import app as application
