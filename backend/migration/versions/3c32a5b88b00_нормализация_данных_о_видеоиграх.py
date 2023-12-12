"""Нормализация данных о видеоиграх

Revision ID: 3c32a5b88b00
Revises: 4c30a3d2fa45
Create Date: 2023-12-11 16:05:02.814135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c32a5b88b00'
down_revision: Union[str, None] = '4c30a3d2fa45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('age_ratings',
    sa.Column('age_rating_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('name_ru', sa.String(length=20), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('age_rating_id')
    )
    op.create_table('g_tags',
    sa.Column('g_tag_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('name_ru', sa.String(length=20), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('g_tag_id')
    )
    op.create_table('genres',
    sa.Column('genre_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('name_ru', sa.String(length=20), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('genre_id')
    )
    op.create_table('platforms',
    sa.Column('platform_id', sa.UUID(), nullable=False),
    sa.Column('parent_platform', sa.String(length=20), nullable=False),
    sa.Column('platform_name', sa.String(length=20), nullable=False),
    sa.Column('platform_slug', sa.String(length=20), nullable=False),
    sa.Column('platform_name_ru', sa.String(length=20), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('platform_id')
    )
    op.create_table('age_rating_games',
    sa.Column('game_id', sa.UUID(), nullable=True),
    sa.Column('age_rating_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['age_rating_id'], ['age_ratings.age_rating_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], ondelete='CASCADE')
    )
    op.create_table('game_genres',
    sa.Column('game_id', sa.UUID(), nullable=True),
    sa.Column('genre_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.genre_id'], ondelete='CASCADE')
    )
    op.create_table('game_platforms',
    sa.Column('game_id', sa.UUID(), nullable=True),
    sa.Column('platform_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['platform_id'], ['platforms.platform_id'], ondelete='CASCADE')
    )
    op.create_table('game_tags',
    sa.Column('game_id', sa.UUID(), nullable=True),
    sa.Column('g_tag_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['g_tag_id'], ['g_tags.g_tag_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], ondelete='CASCADE')
    )
    op.add_column('comments', sa.Column('created', sa.DateTime(timezone=True), nullable=True))
    op.add_column('user_games', sa.Column('user_date', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_games', 'user_date')
    op.drop_column('comments', 'created')
    op.drop_table('game_tags')
    op.drop_table('game_platforms')
    op.drop_table('game_genres')
    op.drop_table('age_rating_games')
    op.drop_table('platforms')
    op.drop_table('genres')
    op.drop_table('g_tags')
    op.drop_table('age_ratings')
    # ### end Alembic commands ###
