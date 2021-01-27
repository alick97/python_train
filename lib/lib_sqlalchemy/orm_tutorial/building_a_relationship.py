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
    # stmt = session.query(
    #     Address.user_id, func.count('*').label('address_count')).group_by(
    #     Address.user_id
    # ).subquery()

    # # print(stmt)

    # # Subquery like a table alias.
    # for u, count in session.query(
    #     User, stmt.c.address_count).outerjoin(
    #         stmt, User.id == stmt.c.user_id
    #         ).order_by(User.id):
    #     print(u, count)

    # Selecting Entities from Subqueries.
    from sqlalchemy.orm import aliased
    stmt = session.query(Address).filter(
        Address.email_address != 'j25@yahoo.com').subquery()
    address_alias = aliased(Address, stmt)
    for user, address in session.query(User, address_alias).join(
        address_alias, User.addresses
    ):
        print(user)
        print(address)


def use_exists():
    # from sqlalchemy.sql import exists
    # stmt = exists().where(Address.user_id == User.id)
    # for name, in session.query(User.name).filter(stmt):
    #     print(name)

    # # Shortcut for exists.
    # for name, in session.query(User.name).filter(
    #         User.addresses.any()):
    #     print(name)

    # # Method any() for many to one.
    # stmt = User.addresses.any(Address.email_address.like('%google%'))
    # for name, in session.query(User.name).filter(stmt):
    #     print(name)

    # # Method has() for one to many. ~ operator mean 'NOT'.
    address_list = session.query(Address).filter(
        ~Address.user.has(User.name == 'jack')
    ).all()
    print(address_list)


def common_relationship_operator():
    # user = session.query(User)[:1][0]
    # query = session.query(Address)
    # address_list = query.filter(Address.user == user).all()
    # address_list = query.filter(Address.user != user).all()
    # address_list = query.filter(Address.user.__eq__(None)).all()
    # print(address_list)

    # address = session.query(Address)[:1][0]
    # address_list = session.query(User).filter(
    #     User.addresses.contains(address),
    #     ).all()
    # print(address_list)

    query = session.query(User)
    user_list = query.filter(User.addresses.any(Address.email_address == 'bar')).all()
    # # also takes keyword arguments:
    # user_list = query.filter(User.addresses.any(email_address='bar')).all()
    print(user_list)

    # address_list = session.query(Address).filter(Address.user.has(name='ed')).all()
    # print(address_list)

    # user = session.query(User)[:1][0]
    # address_list = session.query(Address).with_parent(user, 'addresses').all()
    # print(address_list)


def eager_loading():
    # # Selectin load.
    # # selectinload() tends to be more appropriate for loading related collections.
    # # User.addresses should load eagerly.
    # from sqlalchemy.orm import selectinload
    # jack = session.query(User).options(
    #     selectinload(User.addresses)
    # ).filter_by(name='jack')[0:1][0]
    # print(jack)
    # print(jack.addresses)

    # # Join load.
    # # joinedload() tends to be better suited for many-to-one relationships.
    # from sqlalchemy.orm import joinedload
    # jack = session.query(User).options(
    #     joinedload(User.addresses)
    # ).filter_by(name='jack')[:1][0]
    # print(jack)
    # print(jack.addresses)

    # Explicit Join + Eagerload.
    from sqlalchemy.orm import contains_eager
    jacks_address = session.query(Address).join(
        Address.user
    ).filter(
        User.name == 'jack'
    ).options(
        contains_eager(Address.user)
    ).all()
    print(jacks_address)
    print(jacks_address[0].user)


def main():
    create_table()
    # work_with_related_objects()
    # query_with_joins()
    # query_with_alias()
    # query_with_subquery()
    # use_exists()
    # common_relationship_operator()
    eager_loading()


if __name__ == '__main__':
    main()
