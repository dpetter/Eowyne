from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.schema import Integer, String

from models import Model


class Jahrgang(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Jahrgang"

    id                  = Column(Integer, primary_key = True)
    jahr                = Column(String(4))

    def __init__(self, name):
        self.jahr       = jahr

