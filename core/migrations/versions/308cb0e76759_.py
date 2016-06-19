"""empty message

Revision ID: 308cb0e76759
Revises: 409836b7866e
Create Date: 2016-06-19 05:11:20.466329

"""

# revision identifiers, used by Alembic.
revision = '308cb0e76759'
down_revision = '409836b7866e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=100), nullable=True))
    op.create_unique_constraint(None, 'users', ['password'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'password')
    ### end Alembic commands ###
