from sqlalchemy import Text

from db_labs.db import db


class Skill(db.Model):
    name = db.Column(Text, unique=True, nullable=False)

    developers = db.relationship("Developer", secondary="developer_skill")
