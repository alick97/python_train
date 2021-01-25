from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

from .connection import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    # id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(40))
    nickname = Column(String(40))

    def __repr__(self):
        return f'''<User(id='{self.id}', 'name='{self.name}', fullname='{self.fullname}', \
nickname='{self.nickname}')>'''


def create_table():
    Base.metadata.create_all(engine)


def create_instance_of_mapped_class():
    ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
    print(ed_user.name)
    print(ed_user.id)


def main():
    print(f'table: {User.__table__}')
    create_table()
    create_instance_of_mapped_class()


if __name__ == '__main__':
    main()
