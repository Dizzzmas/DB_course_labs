from typing import Dict, Optional

from jetkit.api import searchable_by, combined_search_by
from flask_smorest import Blueprint, abort
from db_labs.api.developer.decorators import searchable_by_skills
from db_labs.api.developer.schema import DeveloperSchema
from db_labs.db import db
from db_labs.model import Developer, DeveloperSkill, Skill

blp = Blueprint("Developer", __name__, url_prefix=f"/api/developer")


@blp.route("", methods=["GET"])
@blp.response(DeveloperSchema(many=True))
@combined_search_by(
        Developer.first_name, Developer.last_name, search_parameter_name="query",
    )
@searchable_by_skills(search_parameter_name="skills", list_separator=",")
def get_developers():
    developers = (
        Developer.query.join(DeveloperSkill, isouter=True)
            .join(Skill, isouter=True)
    )

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



