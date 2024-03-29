"""empty message

Revision ID: 190f8e6d6b0c
Revises: 
Create Date: 2019-05-21 18:14:05.332395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '190f8e6d6b0c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('surname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_authors_name'), 'authors', ['name'], unique=False)
    op.create_index(op.f('ix_authors_surname'), 'authors', ['surname'], unique=False)
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_name'), 'books', ['name'], unique=False)
    op.create_index(op.f('ix_books_price'), 'books', ['price'], unique=False)
    op.create_index(op.f('ix_books_year'), 'books', ['year'], unique=False)
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genres_name'), 'genres', ['name'], unique=False)
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
    op.create_table('provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('adress', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_adress'), 'provider', ['adress'], unique=False)
    op.create_index(op.f('ix_provider_name'), 'provider', ['name'], unique=False)
    op.create_index(op.f('ix_provider_phone'), 'provider', ['phone'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('surname', sa.String(length=64), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('address', sa.String(length=150), nullable=True),
    sa.Column('isEmployee', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_address'), 'user', ['address'], unique=False)
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_index(op.f('ix_user_phone'), 'user', ['phone'], unique=True)
    op.create_index(op.f('ix_user_surname'), 'user', ['surname'], unique=False)
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
    op.create_table('book_author',
    sa.Column('AuthorId', sa.Integer(), nullable=True),
    sa.Column('BookId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['AuthorId'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['BookId'], ['books.id'], )
    )
    op.create_table('book_genre',
    sa.Column('GenreId', sa.Integer(), nullable=True),
    sa.Column('BookId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BookId'], ['books.id'], ),
    sa.ForeignKeyConstraint(['GenreId'], ['genres.id'], )
    )
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
    op.create_table('warehouse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('BookId', sa.Integer(), nullable=True),
    sa.Column('numberOfBooks', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BookId'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('BookId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('warehouse')
    op.drop_table('pbill')
    op.drop_table('cbill')
    op.drop_table('book_genre')
    op.drop_table('book_author')
    op.drop_table('ProviderPrices')
    op.drop_table('OrderProviderBooks')
    op.drop_table('OrderCustomerBooks')
    op.drop_index(op.f('ix_user_surname'), table_name='user')
    op.drop_index(op.f('ix_user_phone'), table_name='user')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_index(op.f('ix_user_address'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_provider_phone'), table_name='provider')
    op.drop_index(op.f('ix_provider_name'), table_name='provider')
    op.drop_index(op.f('ix_provider_adress'), table_name='provider')
    op.drop_table('provider')
    op.drop_table('orderProvider')
    op.drop_table('orderCustomer')
    op.drop_index(op.f('ix_genres_name'), table_name='genres')
    op.drop_table('genres')
    op.drop_index(op.f('ix_books_year'), table_name='books')
    op.drop_index(op.f('ix_books_price'), table_name='books')
    op.drop_index(op.f('ix_books_name'), table_name='books')
    op.drop_table('books')
    op.drop_index(op.f('ix_authors_surname'), table_name='authors')
    op.drop_index(op.f('ix_authors_name'), table_name='authors')
    op.drop_table('authors')
    # ### end Alembic commands ###
