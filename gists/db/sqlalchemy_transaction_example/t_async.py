import asyncio
import os
from sqlalchemy import create_engine, Column, Integer, String, insert, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Create a base class for declarative class definitions
Base = declarative_base()

# Define a simple model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

script_dir = os.path.dirname(__file__)
rel_path = "example-async.db"
abs_file_path = os.path.join(script_dir, rel_path)
if os.path.exists(abs_file_path):
    os.remove(abs_file_path)
print(f">>>> db file: {abs_file_path}")
# Create an engine and a configured "Session" class
engine = create_async_engine(f'sqlite+aiosqlite:///{abs_file_path}', echo=True)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # session = Session()
    print('=== xxx')
    
    async def _ins_user(name, session):
        insert_stmt = insert(User).values(**{"name": name})
        await session.execute(insert_stmt)

    try:

        # await _ins_user('ccc1')
        # Outer transaction
        # with session.begin_nested():
        async with Session() as session:
            async with session.begin() as trans:
                # insert_stmt = insert(User).values(**{"name": 'cccc21222'})
                # await trans.execute(insert_stmt)
                # Add a user in the outer transaction
                await _ins_user('Alice', session)
                async with session.begin_nested():
                    await _ins_user("A1", session)
                async with session.begin_nested():
                    await _ins_user("A2", session)
                
                # Nested transaction
                # with session.begin_nested():
                # try:
                #   async with session.begin_nested():
                #       # Add another user in the nested transaction
                #       session.add(User(name='Bob'))
                #       # This will raise an exception to demonstrate rollback
                #       raise Exception("Something went wrong in nested transaction")
                # except Exception as e:
                #     pass
                # 
                # # This line would add another user if the nested transaction didn't fail
                # session.add(User(name='Charlie'))
                # session.rollback()
            
            # If we get here, the outer transaction would commit, but since an exception 
            # was raised in the nested transaction, it won't
        # await session.commit()
            users = await session.execute(select(User.name))
            print("Users in database:")
            for user in users:
                print(user)
    except Exception as e:
        print(f"Caught an exception: {e}")
        raise
        # Here, 'Bob' won't be in the database due to the nested transaction rollback, 
        # but 'Alice' will be added if we commit now.
        # session.rollback()
    
    # Let's check what's in the database

    # session.commit()
    # await session.close()

if __name__ == "__main__":
    asyncio.run(main())