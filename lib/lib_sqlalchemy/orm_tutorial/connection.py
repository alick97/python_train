from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

username = 'root'
password = 'example'
host = 'localhost'
database = 'my_schema'

url = f'mysql+pymysql://{username}:{password}@{host}/{database}'

engine = create_engine(url, echo=True)
Session = sessionmaker()
Session.configure(bind=engine)

if __name__ == '__main__':
    engine.connect()
