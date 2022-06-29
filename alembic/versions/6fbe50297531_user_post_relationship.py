"""user-post relationship

Revision ID: 6fbe50297531
Revises: b78b74b5f224
Create Date: 2022-06-29 11:12:12.986466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fbe50297531'
down_revision = 'b78b74b5f224'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','owner_id')
