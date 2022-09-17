from models.model import Base, engine

Base.metadata.create_all(engine)