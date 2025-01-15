import os
from sqlalchemy import create_engine, Column, Integer, String, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a base class for declarative class definitions
Base = declarative_base()

# Define a simple model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

script_dir = os.path.dirname(__file__)
rel_path = "example.db"
abs_file_path = os.path.join(script_dir, rel_path)
if os.path.exists(abs_file_path):
    os.remove(abs_file_path)
print(f">>>> db file: {abs_file_path}")
# Create an engine and a configured "Session" class
engine = create_engine(f'sqlite:///{abs_file_path}', echo=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def main():
    session = Session()
    print('=== xxx')

    try:

        # session.add(User(name='CCC1'))
        
        insert_stmt = insert(User).values(name='CCC1')
        session.execute(insert_stmt)
        session.execute(insert_stmt)
        # Outer transaction
        # with session.begin_nested():
        with session.begin():
            # Add a user in the outer transaction
            session.add(User(name='Alice'))
            
            # Nested transaction
            # with session.begin_nested():
            try:
              with session.begin_nested():
                  # Add another user in the nested transaction
                  session.add(User(name='Bob'))
                  # This will raise an exception to demonstrate rollback
                  raise Exception("Something went wrong in nested transaction")
            except Exception as e:
                pass
            
            # This line would add another user if the nested transaction didn't fail
            session.add(User(name='Charlie'))
            # session.rollback()
        
        # If we get here, the outer transaction would commit, but since an exception 
        # was raised in the nested transaction, it won't
        session.commit()
    except Exception as e:
        print(f"Caught an exception: {e}")
        # Here, 'Bob' won't be in the database due to the nested transaction rollback, 
        # but 'Alice' will be added if we commit now.
        # session.rollback()
    
    # Let's check what's in the database
    users = session.query(User).all()
    print("Users in database:")
    for user in users:
        print(user.name)

    # session.commit()
    session.close()

if __name__ == "__main__":
    main()