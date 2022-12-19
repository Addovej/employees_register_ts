"""initial

Revision ID: 8384e98cf5b7
Revises:
Create Date: 2022-12-19 17:37:45.468239

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8384e98cf5b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_dt', sa.DateTime(), nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=True),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('middle_name', sa.String(length=50), nullable=True),
        sa.Column('position', sa.String(length=25), nullable=True),
        sa.Column('hire_date', sa.Date(), nullable=True),
        sa.Column('salary', sa.Float(), nullable=True),
        sa.Column('chief_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['chief_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('employees')
