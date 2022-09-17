from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///user.db')

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    resumes = relationship("Resume", back_populates="user")


class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    mobile = Column(String)
    github = Column(String)
    linkedin = Column(String)
    summary = Column(String)
    job = Column(String)
    company = Column(String)
    period = Column(String)
    description = Column(String)
    university = Column(String)
    faculty = Column(String)
    GPA = Column(String)
    skills = Column(String)

    user_id = Column(Integer, ForeignKey("user.id"))
    user  = relationship("User", back_populates="resumes")