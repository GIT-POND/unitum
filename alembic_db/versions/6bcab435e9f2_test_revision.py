"""test revision

Revision ID: 6bcab435e9f2
Revises: 
Create Date: 2022-04-28 09:39:46.031233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bcab435e9f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'test_table',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False)
    )
    #DESCRIPTION: CLI command for upgrade   
    # alembic upgrade 6bcab435e9f2

    #DESCRIPTION: CLI command to view current alembic version   
    # alembic current


def downgrade():
    op.drop_table('test_table')
    #DESCRIPTION: CLI command for downgrade     
    # alembic downgrade -1
