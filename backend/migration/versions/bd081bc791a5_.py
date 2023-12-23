"""empty message

Revision ID: bd081bc791a5
Revises:
Create Date: 2023-12-23 23:10:12.983048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd081bc791a5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('cover', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('release', sa.DateTime(), nullable=True),
    sa.Column('playtime', sa.Integer(), nullable=True),
    sa.Column('platform', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('platform_name', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('parent_platform', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('genre', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('tags', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('esrb_rating', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_id'), 'game', ['id'], unique=False)
    op.create_index(op.f('ix_game_slug'), 'game', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game_slug'), table_name='game')
    op.drop_index(op.f('ix_game_id'), table_name='game')
    op.drop_table('game')
    # ### end Alembic commands ###
