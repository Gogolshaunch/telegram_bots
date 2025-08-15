from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column
from sqlalchemy.types import *
from sqlalchemy import or_

engine = create_engine("postgresql+psycopg2://postgres:Mira2008_2020@localhost:5432/owner")
engine2 = create_engine("postgresql+psycopg2://postgres:Mira2008_2020@localhost:5432/finder")

Base = declarative_base()


class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    name = Column(String)
    phonenumber = Column(String)
    tg_user = Column(String)
    city = Column(String)
    type_pet = Column(String)
    name_pet = Column(String)
    sex_pet = Column(Integer)
    breed_pet = Column(String)
    describe = Column(String)
    photo = Column(String)


class Finder(Base):
    __tablename__ = 'finder'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    name = Column(String)
    phonenumber = Column(String)
    tg_user = Column(String)
    city = Column(String)
    type_pet = Column(String)
    name_pet = Column(String)
    sex_pet = Column(Integer)
    breed_pet = Column(String)
    describe = Column(String)
    photo = Column(String)


Base.metadata.create_all(engine)
Base.metadata.create_all(engine2)


def new_human(person, chat_id):
    if person.status == 1:
        with Session(bind=engine2) as session:
            human = Finder(chat_id, person.name, person.phonenumber, person.tg_user, person.city, person.type_pet,
                           person.name_pet, person.sex_pet, person.breed_pet, person.describe, person.photo)
    else:
        with Session(bind=engine) as session:
            human = Owner(chat_id, person.name, person.phonenumber, person.tg_user, person.city, person.type_pet,
                          person.name_pet, person.sex_pet, person.breed_pet, person.describe, person.photo)
    session.add(human)
    session.commit()


def choice_human_owner(person_city, person_type):
    with Session(bind=engine) as session:
        return session.query(Owner).where(or_(Owner.city == person_city, Owner.type_pet == person_type)).all()


def choice_human_finder(person_city, person_type):
    with Session(bind=engine2) as session:
        return session.query(Finder).where(or_(Finder.city == person_city, Finder.type_pet == person_type)).all()


def count_person(status):
    if status == 1:
        with Session(bind=engine2) as session:
            return session.query(Finder).count()
    with Session(bind=engine) as session:
        return session.query(Owner).count()


def del_person(person, chat):
    if person.status == 1:
        with Session(bind=engine2) as session:
            per = session.query(Finder).where(Finder.chat_id == chat).one()
    else:
        with Session(bind=engine) as session:
            per = session.query(Owner).where(Owner.chat_id == chat).one()
    session.delete(per)
    session.commit()
