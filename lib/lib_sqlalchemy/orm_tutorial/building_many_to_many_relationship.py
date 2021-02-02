from sqlalchemy import Table, Text, Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from .declare_a_mapping import Base, create_table, User
from .building_a_relationship import Address
from .connection import Session

session = Session()


# Association table.
post_keywords = Table(
    'post_keywords', Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
)


class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    author = relationship(User, back_populates='posts')

    # many to many BlogPost<->Keyword.
    keywords = relationship('Keyword', secondary=post_keywords, back_populates='posts')

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return f'BlogPost({self.headline}, {self.body}, {self.headline})'


class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost', secondary=post_keywords, back_populates='keywords')

    def __init__(self, keyword):
        self.keyword = keyword


def many_to_many_operator():
    user = session.query(User).filter_by(name='wendy')[:1][0]
    post = BlogPost("Wendy's Blog Post", "This is a test", user)
    session.add(post)

    print(post.keywords)
    post.keywords.append(Keyword('wendy'))
    post.keywords.append(Keyword('firstpost'))

    all_blog_post = session.query(BlogPost).filter(
        BlogPost.keywords.any(keyword='firstpost')
    ).all()
    print(all_blog_post)

    all_blog_post = session.query(BlogPost).filter(
        BlogPost.author == user
    ).filter(
        BlogPost.keywords.any(keyword='firstpost')
    ).all()
    print(all_blog_post)

    # Use quering straight from 'dynamic' relationship.
    all_blog_post = user.posts.filter(
        BlogPost.keywords.any(keyword='firstpost')
    ).all()
    print(all_blog_post)


def main():
    create_table()
    many_to_many_operator()


if __name__ == '__main__':
    main()
