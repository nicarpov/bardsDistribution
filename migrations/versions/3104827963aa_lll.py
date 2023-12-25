"""lll

Revision ID: 3104827963aa
Revises: d7c133809d24
Create Date: 2023-12-25 16:44:20.871532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3104827963aa'
down_revision = 'd7c133809d24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.INTEGER(), nullable=True),
    sa.Column('followed_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###