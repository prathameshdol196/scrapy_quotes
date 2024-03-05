import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create an engine to connect to the MySQL database
engine = create_engine(f'mysql+mysqlconnector://{os.environ["mysql_user"]}:{os.environ["mysql_pass"]}@localhost/quotes')

# Define a base class for declarative class definitions
Base = declarative_base()

# Define the Quote class to represent the quotes table
class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    tags = Column(String(255))

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Query all rows from the quotes table
quotes = session.query(Quote).all()

# Print the retrieved data
for quote in quotes:
    print(quote.id, quote.title, quote.author, quote.tags)

# Close the session
session.close()
