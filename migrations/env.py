from logging.config import fileConfig
import sys
import os

#first set path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# load dotenv
from dotenv import load_dotenv
load_dotenv()

# Then import 
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.models import Base
from alembic import context

target_metadata = Base.metadata