from .declare_a_mapping import User, create_table
from .connection import Session

session = Session()


def user_operator():
    ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
    session.add(ed_user)
    our_user = session.query(User).filter_by(name='ed').first()
    print(ed_user is our_user)

    # Add more users.
    session.add_all([
        User(name='wendy', fullname='Wendy Williams', nickname='windy'),
        User(name='mary', fullname='Mary Contrary', nickname='mary'),
        User(name='fred', fullname='Fred Flintstone', nickname='freddy')])

    # Dirty data.
    ed_user.nickname = 'eddie'
    dirty = session.dirty
    print(f'session dirty data: {dirty}')

    # New data.
    new_data = session.new
    print(f'session new data: {new_data}')

    session.commit()

    # Rolling back.
    ed_user.name = 'Edwardo'
    fake_user = User(name='fakeuser', fullname='Invalid', nickname='12345')
    session.add(fake_user)
    users = session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
    print(f'users: {users}')

    session.rollback()
    print(f'ed_user.name: {ed_user.name}')
    is_fake_user_exist = fake_user in session
    print(f'is fake user in session: {is_fake_user_exist}')


def main():
    create_table()
    user_operator()


if __name__ == '__main__':
    main()
