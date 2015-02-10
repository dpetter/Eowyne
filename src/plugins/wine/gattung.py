from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from  models import Model


class Gattung(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Gattung"

    id                  = Column(Integer, primary_key = True)
    name                = Column(String(255))

    def __init__(self, name):
        self.name       = name

