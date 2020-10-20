from sqlalchemy import ForeignKey, Integer

from db_labs.db import db


class DeveloperSkill(db.Model):

    developer_id = db.Column(Integer, ForeignKey("developer.id", on_delete="CASCADE"), nullable=False)
    skill_id = db.Column(Integer, ForeignKey("skill.id", on_delete="CASCADE"), nullable=False)