from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# Working with Database Metadata
from sqlalchemy import MetaData
metadata_obj = MetaData()

from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

# demonstrative print statements
# print(repr(user_table.c.id))
# print(user_table.c.name)
# print(user_table.c.keys())

#Declaring Simple Constraints¶
# print(user_table.primary_key)

from sqlalchemy import ForeignKey, select
address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

#Emitting DDL to the Database¶
metadata_obj.create_all(engine)

#Using ORM Declarative Forms to Define Table Metadata¶
# -- > Establishing a Declarative Base¶
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

# --> Declaring Mapped Classes¶
# from typing import List --> List[T] = list[T]
# from typing import Optional --> Optional[T] = T | None
# the above is commented out due to changes in example to update syntax
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

print('Creating tables from Base metadata')
Base.metadata.create_all(engine)

# Data Manipulation with the ORM¶
# --> Inserting Rows using the ORM Unit of Work pattern¶
# ----> Instances of Classes represent Rows¶
squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
# print(squidward)
# --> Adding objects to a Session¶
from sqlalchemy.orm import Session
session = Session(engine)
session.add(squidward)
session.add(krabs)
session.new
# print("HERE ", squidward)
# --> Flushing
session.flush()
# print("HERE ", krabs)
# --> Getting Objects by Primary Key from the Identity Map¶
some_squidward = session.get(User, 1)
print(some_squidward)
print(some_squidward is squidward)
#--> Committing
session.commit()
print(some_squidward)

#TODO
sb = User(name="spongebob", fullname="Spongebob Squarepants")
sandy = User(name="sandy", fullname="Sandy Cheeks")
pat = User(name="patrick", fullname="Patrick Star")
session.add(sb)
session.add(sandy)
session.add(pat)
session.new
session.flush()
session.commit()

# Updating ORM Objects using the Unit of Work pattern¶
sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
session.flush()

# rushed
from sqlalchemy import select
stmt = select(user_table).where(user_table.c.name == "spongebob")
print(stmt)

# with engine.connect() as conn:
#     for row in conn.execute(stmt):
#         print(row)

stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)