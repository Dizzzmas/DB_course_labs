from jetkit.api import searchable_by, combined_search_by
from smorest_crud import CollectionView
from flask_smorest import Blueprint
from db_labs.api.developer.decorators import searchable_by_skills
from db_labs.api.developer.schema import DeveloperSchema
from db_labs.model import Developer, DeveloperSkill, Skill

blp = Blueprint("Developer", __name__, url_prefix=f"/developer")


@blp.route("")
class DeveloperCollection(CollectionView):
    model = Developer
    prefetch = [Developer.skills]

    list_enabled = True
    create_enabled = True

    @blp.response(DeveloperSchema(many=True))
    @combined_search_by(
        Developer.full_name, Developer.seniority, search_parameter_name="query",
    )
    @searchable_by(Developer.first_name, search_parameter_name="first_name")
    @searchable_by_skills(search_parameter_name="skills", list_separator=",")
    def get(self):
        developers = (
            Developer.query.join(DeveloperSkill, isouter=True)
            .join(Skill, isouter=True)
            .all()
        )

        return developers


@blp.route("get-developers", methods=["POST"])
@blp.response(DeveloperSchema(many=True))
def generate_s3_cv_upload_link():
    pass
