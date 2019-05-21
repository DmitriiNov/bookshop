"""empty message

Revision ID: c52ff3a18401
Revises: 2b0c1daaadb4
Create Date: 2019-05-21 16:31:43.245299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c52ff3a18401'
down_revision = '2b0c1daaadb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cbill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('OrderCId', sa.Integer(), nullable=True),
    sa.Column('sum', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['OrderCId'], ['orderCustomer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('OrderCId')
    )
    op.create_table('pbill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('OrderPId', sa.Integer(), nullable=True),
    sa.Column('sum', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['OrderPId'], ['orderProvider.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('OrderPId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pbill')
    op.drop_table('cbill')
    # ### end Alembic commands ###
