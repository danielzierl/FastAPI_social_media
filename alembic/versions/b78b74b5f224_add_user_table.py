"""add user table

Revision ID: b78b74b5f224
Revises: 9ecdfc23532e
Create Date: 2022-06-29 10:35:52.991175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b78b74b5f224'
down_revision = '917a4836ad7d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')

                    )


def downgrade() -> None:
    op.drop_table('users')

