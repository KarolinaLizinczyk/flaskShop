"""empty message

Revision ID: 834538ed337a
Revises: ddf0e6d2a2f3
Create Date: 2017-08-08 22:05:45.728000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '834538ed337a'
down_revision = 'ddf0e6d2a2f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('checkout', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'checkout')
    # ### end Alembic commands ###
