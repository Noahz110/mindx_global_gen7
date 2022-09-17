from sqlalchemy.orm import sessionmaker
from models.model import Base, engine, User, Resume

Session = sessionmaker(bind = engine)

session = Session()

# user = User(name = 'dang111296', password = '123456')
# session.add(user)
# session.commit()

# c = session.query(User).filter(User.name == "dang111296").first()
# print(c.password)
# c = session.query(Resume).filter(Resume.id == 1).first()
# print(c.id)