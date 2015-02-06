#from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime, String, Text

from models import Model
from sqlalchemy.orm import relationship


class Blog(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Blog"
    
    id                  = Column(Integer, primary_key = True)
    createdOn           = Column(DateTime)
    changedOn           = Column(DateTime)
    author_id           = Column(Integer, ForeignKey("Users.id"))
    author              = relationship("Editor")
    title               = Column(String(255))
    description         = Column(Text)
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, author_id = 0, title = None, description = None):
        self.author_id = author_id
        self.title = title
        self.description = description