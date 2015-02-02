#from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime, String, Text

from models import Model


class Blog(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Blog"
    
    id                  = Column(Integer, primary_key = True)
    createdOn           = Column(DateTime)
    changedOn           = Column(DateTime)
    author_id           = Column(Integer, ForeignKey("Users.id"))
#    author              = relationship()
    title               = Column(String(255))
    content             = Column(Text)