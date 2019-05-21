"""empty message

Revision ID: 900fb05fe8c1
Revises: 5c511f9e6aa1
Create Date: 2019-05-21 15:35:45.067362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '900fb05fe8c1'
down_revision = '5c511f9e6aa1'
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
    op.create_table('BookAuthor',
    sa.Column('AuthorId', sa.Integer(), nullable=True),
    sa.Column('BookIdooo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['AuthorId'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['BookIdooo'], ['books.id'], )
    )
    op.drop_index('ix_author_name', table_name='author')
    op.drop_index('ix_author_surname', table_name='author')
    op.drop_table('author')
    op.drop_index('ix_book_name', table_name='book')
    op.drop_index('ix_book_price', table_name='book')
    op.drop_index('ix_book_year', table_name='book')
    op.drop_table('book')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('price', sa.INTEGER(), nullable=True),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_book_year', 'book', ['year'], unique=False)
    op.create_index('ix_book_price', 'book', ['price'], unique=False)
    op.create_index('ix_book_name', 'book', ['name'], unique=False)
    op.create_table('author',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('surname', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_author_surname', 'author', ['surname'], unique=False)
    op.create_index('ix_author_name', 'author', ['name'], unique=False)
    op.drop_table('BookAuthor')
    op.drop_index(op.f('ix_books_year'), table_name='books')
    op.drop_index(op.f('ix_books_price'), table_name='books')
    op.drop_index(op.f('ix_books_name'), table_name='books')
    op.drop_table('books')
    op.drop_index(op.f('ix_authors_surname'), table_name='authors')
    op.drop_index(op.f('ix_authors_name'), table_name='authors')
    op.drop_table('authors')
    # ### end Alembic commands ###