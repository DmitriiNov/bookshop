"""empty message

Revision ID: 2b0c1daaadb4
Revises: c1a3435f800b
Create Date: 2019-05-21 16:06:54.785875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b0c1daaadb4'
down_revision = 'c1a3435f800b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orderCustomer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('CustomerId', sa.Integer(), nullable=True),
    sa.Column('EmployeeId', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orderProvider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ProviderId', sa.Integer(), nullable=True),
    sa.Column('EmployeeId', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('OrderCustomerBooks',
    sa.Column('OrderCId', sa.Integer(), nullable=True),
    sa.Column('BookId', sa.Integer(), nullable=True),
    sa.Column('numberOfBooks', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BookId'], ['books.id'], ),
    sa.ForeignKeyConstraint(['OrderCId'], ['orderCustomer.id'], )
    )
    op.create_table('OrderProviderBooks',
    sa.Column('OrderPId', sa.Integer(), nullable=True),
    sa.Column('BookId', sa.Integer(), nullable=True),
    sa.Column('numberOfBooks', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BookId'], ['books.id'], ),
    sa.ForeignKeyConstraint(['OrderPId'], ['orderProvider.id'], )
    )
    op.create_table('ProviderPrices',
    sa.Column('ProviderId', sa.Integer(), nullable=True),
    sa.Column('BookId', sa.Integer(), nullable=True),
    sa.Column('Price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BookId'], ['books.id'], ),
    sa.ForeignKeyConstraint(['ProviderId'], ['provider.id'], )
    )
    op.drop_table('order_to_provider')
    op.drop_table('order_from_customer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_from_customer',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('CustomerId', sa.INTEGER(), nullable=True),
    sa.Column('EmployeeId', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_to_provider',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ProviderId', sa.INTEGER(), nullable=True),
    sa.Column('EmployeeId', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('ProviderPrices')
    op.drop_table('OrderProviderBooks')
    op.drop_table('OrderCustomerBooks')
    op.drop_table('orderProvider')
    op.drop_table('orderCustomer')
    # ### end Alembic commands ###