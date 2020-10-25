from typing import Dict, Optional

from flask import request
from jetkit.api import searchable_by, combined_search_by
from flask_smorest import Blueprint, abort
from sqlalchemy import text
from sqlalchemy.orm import joinedload

from db_labs.api.developer.decorators import searchable_by_skills
from db_labs.api.developer.schema import DeveloperSchema
from db_labs.db import db
from db_labs.model import Developer, DeveloperSkill, Skill

blp = Blueprint("Developer", __name__, url_prefix=f"/api/developer")


@blp.route("", methods=["GET"])
@blp.response(DeveloperSchema(many=True))
# @combined_search_by(  # For use with ORM
#     Developer.first_name,
#     Developer.last_name,
#     Skill.name,
#     search_parameter_name="query",
# )
def get_developers():
    query_string = request.args.get("query")

    if query_string:
        query_string = f"%{query_string}%"  # Enclosed in '%' as per ILIKE syntax

        query = text(
            """SELECT * 
FROM developer LEFT OUTER JOIN developer_skill ON developer.id = developer_skill.developer_id LEFT OUTER JOIN skill ON skill.id = developer_skill.skill_id LEFT OUTER JOIN vacancy AS vacancy_1 ON vacancy_1.id = developer.vacancy_id LEFT OUTER JOIN (developer_skill AS developer_skill_1 JOIN skill AS skill_1 ON skill_1.id = developer_skill_1.skill_id) ON developer.id = developer_skill_1.developer_id 
WHERE CAST(developer.first_name AS VARCHAR) ILIKE :query_string ESCAPE '~' OR CAST(developer.last_name AS VARCHAR) ILIKE :query_string ESCAPE '~' OR CAST(skill.name AS VARCHAR) ILIKE :query_string ESCAPE '~'"""
        )
        developers = db.session.execute(query, dict(query_string=query_string))
    else:
        query = """SELECT * FROM developer LEFT OUTER JOIN developer_skill ON developer.id = developer_skill.developer_id LEFT OUTER JOIN skill ON skill.id = developer_skill.skill_id LEFT OUTER JOIN vacancy AS vacancy_1 ON vacancy_1.id = developer.vacancy_id LEFT OUTER JOIN (developer_skill AS developer_skill_1 JOIN skill AS skill_1 ON skill_1.id = developer_skill_1.skill_id) ON developer.id = developer_skill_1.developer_id"""
        developers = db.session.execute(query)

    # developers = (
    #     Developer.query.join(DeveloperSkill, isouter=True)
    #     .join(Skill, isouter=True)
    #     .options(joinedload(Developer.skills), joinedload(Developer.vacancy))
    # )

    return developers


@blp.route("", methods=["POST"])
@blp.response(DeveloperSchema)
@blp.arguments(DeveloperSchema)
def create_developer(args: Dict[str, str]):
    developer = Developer(**args)

    db.session.add(developer)

    db.session.commit()

    return developer


@blp.route("/<string:developer_id>", methods=["PATCH"])
@blp.response(DeveloperSchema)
@blp.arguments(DeveloperSchema)
def update_developer(args: Dict[str, str], developer_id: int):
    """Check if developer with given id exists, then update the entry."""
    developer = Developer.query.get(developer_id)

    if not developer:
        abort(404, message=f"No developer with id: ${developer_id} found.")

    # remove None values so they do not override existing data
    values = {key: value for key, value in args.items() if value is not None}

    Developer.query.update(values)

    db.session.commit()

    return developer
