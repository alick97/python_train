# link: https://docs.sqlalchemy.org/en/13/orm/tutorial.html#building-a-relationship.
from sqlalchemy import ForeignKey, Integer, String, Column, func
from sqlalchemy.orm import relationship

from .declare_a_mapping import Base, create_table, User
from .connection import Session

session = Session()


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='addresses')

    def __repr__(self):
        return f"<Address(email_address='{self.email_address}')>"


def work_with_related_objects():
    jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
    print(jack.addresses)

    # Assign a full list directly.
    jack.addresses = [
        Address(email_address='jack@google.com'),
        Address(email_address='j25@yahoo.com')
    ]
    # When using a bidirectional relationship, elements added in one direction
    # automatically become visible in the other direction.
    # This behavior occurs based on attribute on-change events and
    # is evaluated in Python, without using any SQL:
    print(jack.addresses[1])
    print(jack.addresses[1].user)

    session.add(jack)
    session.commit()

    jack = session.query(User).filter_by(id=jack.id).one()
    print(jack.addresses)


def query_with_joins():
    # # Inner join.
    # query = session.query(
    #     User, Address).filter(
    #         User.id == Address.user_id).filter(
    #             Address.email_address == 'jack@google.com'
    #         )
    # all_user_address = query.all()
    # for u, a in all_user_address:
    #     print(u)
    #     print(a)

    # # Inner join.
    # all_users = session.query(User).join(Address).\
    #     filter(Address.email_address == 'jack@google.com').\
    #     all()
    # for u in all_users:
    #     print(u)

    # # Explicit join condition.
    # all_users = session.query(User).join(Address, User.id == Address.user_id).all()
    # print(all_users)

    # # Specify relationship from left to right.
    # all_users = session.query(User).join(User.addresses).all()
    # print(all_users)

    # # Same, with explicit ta`rget.
    # all_users = session.query(User).join(Address, User.addresses).all()
    # print(all_users)

    # Left outer join.
    # all_users = session.query(User).outerjoin(User.addresses)
    # all_users = session.query(User).outerjoin(Address).all()
    # print(all_users)

    # Multiple entities select_from control which is left and which is right.
    # TODO: Need more example for join with select_from.
    query = session.query(User, Address).select_from(Address).join(User)
    print(query)


def query_with_alias():
    from sqlalchemy.orm import aliased
    address_alias1 = aliased(Address)
    address_alias2 = aliased(Address)
    for user_name, email1, email2 in \
        session.query(User.name, address_alias1.email_address, address_alias2.email_address).\
        join(User.addresses.of_type(address_alias1)).\
        join(User.addresses.of_type(address_alias2)).\
        filter(address_alias1.email_address == 'jack@google.com').\
        filter(address_alias2.email_address == 'j25@yahoo.com'):
        print(user_name, email1, email2)

    query = session.query(User).join(address_alias1).\
        join(address_alias2).\
        filter(address_alias1.email_address == 'jack@google.com').\
        filter(address_alias2.email_address == 'j25@yahoo.com')
    print(query.all())


def query_with_subquery():
    # # Subquery: it’s actually shorthand for query.statement.alias().
    stmt = session.query(
        Address.user_id, func.count('*').label('address_count')).group_by(
        Address.user_id
    ).subquery()

    # print(stmt)

    # Subquery like a table alias.
    for u, count in session.query(
        User, stmt.c.address_count).outerjoin(
            stmt, User.id == stmt.c.user_id
            ).order_by(User.id):
        print(u, count)


def main():
    create_table()
    # work_with_related_objects()
    # query_with_joins()
    # query_with_alias()
    query_with_subquery()


if __name__ == '__main__':
    main()
