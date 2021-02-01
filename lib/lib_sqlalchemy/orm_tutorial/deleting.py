from sqlalchemy.ext.declarative import declarative_base
from .connection import engine, Session
from .declare_a_mapping import User, create_table
from .building_a_relationship import Address

Base = declarative_base()
session = Session()


def delete_model():
    # Case, delete user, but user's address is not deleted cascade.
    # Need config like below in users:
    # addresses = relationship("Address", back_populates='user',
    #                     cascade="all, delete, delete-orphan")
    # Note:
    #     https://docs.sqlalchemy.org/en/13/orm/cascades.html#unitofwork-cascades.
    #     https://docs.sqlalchemy.org/en/13/orm/cascades.html#passive-deletes.
    ed_user = User(name='user_for_delete', fullname='Ed Jones', nickname='edsnickname')
    # Assign a full list directly.
    ed_user.addresses = [
        Address(email_address='user_for_delete@google.com'),
        Address(email_address='user_for_delete@google.com')
    ]
    session.add(ed_user)
    session.commit()

    del ed_user.addresses[0]
    session.commit()

    session.delete(ed_user)
    session.commit()
    count_delete_user = session.query(User).filter_by(name='user_for_delete').count()
    print(count_delete_user)

    count_address = session.query(Address).filter(
        Address.email_address.in_(['user_for_delete@google.com'])
    ).count()
    print(f'cascade address count: {count_address}')


def main():
    create_table()
    delete_model()


if __name__ == '__main__':
    main()
