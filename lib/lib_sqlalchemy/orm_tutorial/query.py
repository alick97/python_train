from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .connection import Session
from .declare_a_mapping import User, create_table

session = Session()


def qs_users_order_by():
    users = session.query(User).order_by(User.id).all()
    for u in users:
        print(f'id: {u.id}, name: {u.name}, fullname: {u.fullname}')


def qs_by_column():
    # Show column.
    qs = session.query(User.name, User.fullname).all()
    for name, nickname in qs:
        print(f'name: {name}, nickname: {nickname}')


def qs_by_namedtuples():
    qs = session.query(User, User.name).all()
    for row in qs:
        print(row.User, row[1], row.name)


def qs_by_label():
    qs = session.query(User.name.label('name_label')).all()
    for row in qs:
        print(row.name_label)


def qs_by_alias():
    user_alias = aliased(User, name='user_alias')

    for row in session.query(user_alias, user_alias.name).all():
        print(row.user_alias, row.name)


def qs_limit_offset():
    qs = session.query(User).order_by(User.id)[2:6]
    for u in qs:
        print(u)


def qs_filter():
    # qs = session.query(User.name).filter_by(fullname='Ed Jones', name='ed')
    # for name, in qs:
    #     print(name)

    # qs = session.query(User.name).filter(User.fullname == 'Ed Jones', User.name == 'ed')
    # for name, in qs:
    #     print(name)

    # for user in session.query(User).filter(User.name == 'ed').filter(User.fullname == 'Ed Jones'):
    #     print(user)

    # Common filter operators.
    # qs1 = session.query(User).filter(User.name != 'ed').all()
    # print(qs1)

    # qs2 = session.query(User).filter(User.name.like('%ed%')).all()
    # print(qs2)

    # qs3 = session.query(User).filter(User.name.ilike('%ed%')).all()
    # print(qs3)

    # IN.
    # qs = session.query(User)
    # qs = qs.filter(User.name.in_(['ed', 'wendy', 'jack']))
    # print(qs)

    # works with query objects too:
    # qs = session.query(User).filter(User.name.in_(
    #     session.query(User.name).filter(User.name.like('%ed%'))
    # ))
    # print(qs)

    # use tuple_() for composite (multi-column) queries
    # from sqlalchemy import tuple_
    # qs = session.query(User).filter(
    #     tuple_(User.name, User.nickname).in_(
    #         [('ed', 'edsnickname'), ('wendy', 'windy')]))
    # print(qs)

    # Not in.
    # qs = session.query(User).filter(~User.name.in_(['ed', 'wendy', 'jack']))
    # print(qs)

    # None.
    # qs = session.query(User).filter(User.name == None)
    # qs = session.query(User).filter(User.name.is_(None))
    # qs = session.query(User).filter(User.name != None)
    # qs = session.query(User).filter(User.name.isnot(None))
    # print(qs)

    # And.
    # from sqlalchemy import and_
    # query = session.query(User)
    # qs = query.filter(and_(
    #      User.name == 'ed', User.fullname == 'Ed Jones'
    # ))

    # or send multiple expressions to .filter()
    # qs = query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

    # or chain multiple filter()/filter_by() calls
    # qs = query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')

    # print(qs)

    # Or.
    # from sqlalchemy import or_
    # query = session.query(User)
    # qs = query.filter(or_(
    #     User.name == 'ed', User.name == 'wendy'
    # ))
    # print(qs)

    # Match.
    # https://www.mysqltutorial.org/mysql-boolean-text-searches.aspx
    # https://stackoverflow.com/questions/18035795/sql-error-1191-cant-find-fulltext-index-matching-the-column-list
    # need run sql to add FULLTEXT index:
    # ALTER TABLE table ADD FULLTEXT index_name(column1);
    # MySQL Boolean full-text search operators
    # The following table illustrates the full-text search Boolean operators and their meanings:

    # Operator	Description
    # +	Include, the word must be present.
    # –	Exclude, the word must not be present.
    # >	Include, and increase ranking value.
    # <	Include, and decrease the ranking value.
    # ()	Group words into subexpressions (allowing them to be included, excluded, ranked, and so forth as a group).
    # ~	Negate a word’s ranking value.
    # *	Wildcard at the end of the word.
    # “”	Defines a phrase (as opposed to a list of individual words, the entire phrase is matched for inclusion or exclusion).
    # qs = session.query(User).filter(User.name.match('wen* -wendy'))
    qs = session.query(User).filter(User.name.match('wen*'))
    from sqlalchemy.dialects import mysql
    # print(qs.statement)
    print(qs.statement.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True}))
    print(qs.all())


def qs_list_scalar():
    '''Returning Lists and Scalars'''
    query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
    all_list = query.all()
    print(all_list)
    print(query.first())
    try:
        query.one()
    except MultipleResultsFound as e:
        print(f'type: {type(e)}, content: {e}')

    try:
        user = query.filter(User.id == -1).one()
        print(user)
    except NoResultFound as e:
        print(f'type: {type(e)}, content: {e}')

    u = query.filter(User.id == -1).one_or_none()
    print(f'u: {u}')

    query = session.query(User.id).filter(User.id == 5).order_by(User.id)
    value = query.scalar()
    print(f'user id: {value}, can be None if not found, found multi will raise.')


def qs_by_text():
    from sqlalchemy import text
    # query = session.query(User).filter(text('id < 224')).order_by(text('id'))
    # users = query.all()
    # for u in users:
    #     print(f'id: {u.id}, name: {u.name}')

    # Bind parameters.
    # query = session.query(User).filter(text('id<:value and name=:name')).params(
    #     value=244, name='fred'
    # ).order_by(User.id)
    # print(query.first())
    # query = session.query(User).from_statement(
    #     text('select * from users where name=:name')
    # ).params(
    #     name='ed'
    # )
    # print(query.all())

    # # Map column position to model.
    # stmt = text("SELECT name, id, fullname, nickname FROM users where name=:name")
    # stmt = stmt.columns(User.name, User.id, User.fullname, User.nickname)
    # users = session.query(User).from_statement(stmt).params(name='ed').all()
    # print(users)

    # Explict column.
    stmt = text("SELECT name, id FROM users where name=:name")
    stmt = stmt.columns(User.name, User.id)  # Note: will map stmt name -> User.name, id -> User.id.
    # stmt = stmt.columns(User.id, User.name)  # Note: will map stmt name -> User.id,  id -> User.name.
    user_info_list = session.query(User.id, User.name).from_statement(stmt).params(
        name='ed'
    ).all()
    for row in user_info_list:
        print(row)


def qs_counting():
    from sqlalchemy import func
    # count = session.query(User).filter(User.name.like('%ed')).count()
    # print(count)

    count = session.query(func.count('*')).select_from(User).scalar()
    print(count)
    count = session.query(func.count('1')).select_from(User).scalar()
    print(count)

    # user_count_list = session.query(func.count(User.name), User.name).group_by(User.name).all()
    # print(user_count_list)


def main():
    create_table()
    # qs_users_order_by()
    # qs_by_column()
    # qs_by_namedtuples()
    # qs_by_label()
    # qs_by_alias()
    # qs_limit_offset()
    # qs_filter()
    # qs_list_scalar()
    # qs_by_text()
    qs_counting()


if __name__ == '__main__':
    main()
