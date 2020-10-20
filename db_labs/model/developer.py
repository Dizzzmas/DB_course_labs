from jetkit.db.model import TSTZ
from sqlalchemy import Integer, ForeignKey, Text

from db_labs.db import db


class Developer(db.Model):

    first_name = db.Column(Text)
    last_name = db.Column(Text)
    email = db.Column(Text)
    birthdate = db.Column(TSTZ)

    vacancy_id = db.Column(Integer, ForeignKey("vacancy.id", ondelete="SET NULL"))
    vacancy = db.relationship("Vacancy", back_populates="developers")

    skills = db.relationship("Skill", secondary="developer_skill")
