from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from models import Model


class Region(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Region"

    id                  = Column(Integer, primary_key = True)
    name                = Columnl(String(255))

    def __init__(self, name):
        self.name       = name

