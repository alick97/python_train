from sqlalchemy import create_engine

username = 'root'
password = 'example'
host = 'localhost'
database = 'my_schema'

url = f'mysql+pymysql://{username}:{password}@{host}/{database}'

engine = create_engine(url, echo=True)

if __name__ == '__main__':
    engine.connect()
