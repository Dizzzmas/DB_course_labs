"""Add trgm indexes for faster search

Revision ID: 89c3265cccbc
Revises: 32adfebb0d49
Create Date: 2020-10-25 22:12:33.422891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89c3265cccbc'
down_revision = '32adfebb0d49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm";')
    op.create_index('developer_first_name_trgm_idx', 'developer', ['first_name'], unique=False, postgresql_using='gin', postgresql_ops={'first_name': 'gin_trgm_ops'})
    op.create_index('developer_last_name_trgm_idx', 'developer', ['last_name'], unique=False, postgresql_using='gin', postgresql_ops={'last_name': 'gin_trgm_ops'})
    op.create_index('unique_developer_id_skill_id_idx', 'developer_skill', ['developer_id', 'skill_id'], unique=True)
    op.create_index('skill_name_trgm_idx', 'skill', ['name'], unique=False, postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'})
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('skill_name_trgm_idx', table_name='skill')
    op.drop_index('unique_developer_id_skill_id_idx', table_name='developer_skill')
    op.drop_index('developer_last_name_trgm_idx', table_name='developer')
    op.drop_index('developer_first_name_trgm_idx', table_name='developer')
    # ### end Alembic commands ###
