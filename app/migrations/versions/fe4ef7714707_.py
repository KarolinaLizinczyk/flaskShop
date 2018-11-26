"""empty message

Revision ID: fe4ef7714707
Revises: 032534d8b66f
Create Date: 2017-08-14 13:12:48.401000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe4ef7714707'
down_revision = '032534d8b66f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('total_price', sa.Numeric(precision=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'total_price')
    # ### end Alembic commands ###