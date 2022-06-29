"""create table

Revision ID: 917a4836ad7d
Revises: 
Create Date: 2022-06-29 10:09:09.782075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '917a4836ad7d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',sa.Integer,nullable=False,primary_key=True),
                    sa.Column('title',sa.String, nullable=False))
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    op.add_column('posts', sa.Column('published', type_=sa.Boolean, nullable=True, server_default='TRUE'))
    op.add_column('posts',
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_table('posts')

    pass
