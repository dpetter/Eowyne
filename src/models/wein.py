from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from models import Model


class Wein(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Wein"

    id                  = Column(Integer, primary_key = True)
    name                = Column(String(255))
    gattung_id          = Column(Integer, ForeignKey("Gattung.id"))
    gattung             = relationship('Gattung',
            backref=backref('Wein', lazy='dynamic'))
    rebsorte_id         = Column(Integer, ForeignKey("Rebsorte.id"))
    rebsorte            = relationship('Rebsorte',
            backref=backref('Wein', lazy='dynamic'))
    land_id             = Column(Integer, ForeignKey("Land.id"))
    land                = relationship("Land",
            backref=backref('Wein', lazy='dynamic'))
    region_id           = Column(Integer, ForeignKey("Region.id"))
    region              = relationship("Region",
            backref=backref('Wein', lazy='dynamic'))
    weingut_id          = Column(Integer, ForeignKey("Weingut.id"))
    weingut             = relationship("Weingut",
            backref=backref('Wein', lazy='dynamic'))
    jahrgang_id         = Column(Integer, ForeignKey("Jahrgang.id"))
    jahrgang            = relationship("Jahrgang",
            backref=backref('Wein', lazy='dynamic'))

    def __init__(self, name = None, gattung = None, rebsorte = None,
            land = None, region = None, weingut = None, jahrgang = None):
        self.name       = name
        self.gattung    = gattung
        self.rebsorte   = rebsorte
        self.land       = land
        self.region     = region
        self.weingut    = weingut
        self.jahrgang   = jahrgang

