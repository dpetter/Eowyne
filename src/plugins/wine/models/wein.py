from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger, Text

from core.shared import db
from models import Model


class Wein(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Wein"

    id                  = Column(Integer, primary_key = True)
    name                = Column(String(255))
    gattung_id          = Column(Integer, ForeignKey("Gattung.id"))
    gattung             = db.relationship('Gattung',
            backref=db.backref('Wein', lazy='dynamic'))
    rebsorte_id         = Column(Integer, ForeignKey("Rebsorte.id"))
    rebsorte            = db.relationship('Rebsorte',
            backref=db.backref('Wein', lazy='dynamic'))
    land_id             = Column(Integer, ForeignKey("Land.id"))
    land                = db.relationship("Land",
            backref=db.backref('Wein', lazy='dynamic'))
    region_id           = Column(Integer, ForeignKey("Region.id"))
    region              = db.relationship("Region",
            backref=db.backref('Wein', lazy='dynamic'))
    weingut_id          = Column(Integer, ForeignKey("Weingut.id"))
    weingut             = db.relationship("Weingut",
            backref=db.backref('Wein', lazy='dynamic'))
    jahrgang            = Column(SmallInteger)
    beschreibung        = Column(Text)

    def __init__(self, name = None, gattung = None, rebsorte = None,
            land = None, region = None, weingut = None, jahrgang = None,
            beschreibung = None):
        self.name       = name
        self.gattung    = gattung
        self.rebsorte   = rebsorte
        self.land       = land
        self.region     = region
        self.weingut    = weingut
        self.jahrgang   = jahrgang
        self.beschreibung = beschreibung

    def __str__(self):
        return "Wein '%s'" % (self.name)
