from sqlalchemy import create_engine, Column, String, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Hist(Base):
    __tablename__ = 'generation_history'

    id = Column(String, primary_key=True)
    username = Column(String)
    timestamp = Column(TIMESTAMP)
    artist = Column(String)
    tags = Column(String)

class Metadata(Base):
    __tablename__ = 'metadata'

    id = Column(String, primary_key=True)
    timestamp = Column(TIMESTAMP)
    duration = Column(Integer)


# Step 3: Specify the directory where the DB will be kept
db_directory = 'static/databases'
db_file = 'db_lastfm_persistent.db'
db_path = os.path.join(db_directory, db_file)

# Ensure the directory exists
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# Step 4: Create an SQLite database with the specified directory and connect to it
engine = create_engine(f'sqlite:///{db_path}')

# Step 5: Create the table(s) in the database
Base.metadata.create_all(engine)

# Step 6: Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

def add_to_hist_db(id: str, username: str, timestamp: "datetime", artist: str, tags: str):

    """
    Method that adds data to History generation table for end-users

    Args:
        id: uuid4 generated ID
        timestamp: time when generation happened
        artist: name of the artist that was generated
        tags: tags for that artist
    """

    session.add(Hist(id=id, username=username, timestamp=timestamp, artist=artist, tags=tags))
    session.commit()

