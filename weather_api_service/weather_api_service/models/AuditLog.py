from weather_api_service import db

"""
Model classes for auditing top queried records
"""

class AuditRecord(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hits = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    lastUpdateTimestamp = db.Column(db.String(255), nullable=False)


class AuditUser(AuditRecord):
    __tablename__ = 'AuditUsers'


class AuditCity(AuditRecord):
    __tablename__ = 'AuditCities'


class AuditCountry(AuditRecord):
    __tablename__ = 'AuditCountries'
