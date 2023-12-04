"""empty message

Revision ID: 9d9402b0ccff
Revises: d8b23db4f1bc
Create Date: 2023-12-04 21:11:33.616687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d9402b0ccff'
down_revision: Union[str, None] = 'd8b23db4f1bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('boards_user_id_fkey', 'boards', type_='foreignkey')
    op.create_foreign_key(None, 'boards', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('posts_board_id_fkey', 'posts', type_='foreignkey')
    op.drop_constraint('posts_user_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'boards', ['board_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'posts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_user_id_fkey', 'posts', 'users', ['user_id'], ['id'])
    op.create_foreign_key('posts_board_id_fkey', 'posts', 'boards', ['board_id'], ['id'])
    op.drop_constraint(None, 'boards', type_='foreignkey')
    op.create_foreign_key('boards_user_id_fkey', 'boards', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
