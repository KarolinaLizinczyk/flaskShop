"""empty message

Revision ID: efcf64e320e3
Revises: 2cd68922ebd5
Create Date: 2017-08-01 23:37:51.701000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efcf64e320e3'
down_revision = '2cd68922ebd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shop_user', sa.Column('image_filename', sa.String(), nullable=True))
    op.add_column('shop_user', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shop_user', 'image_url')
    op.drop_column('shop_user', 'image_filename')
    # ### end Alembic commands ###
