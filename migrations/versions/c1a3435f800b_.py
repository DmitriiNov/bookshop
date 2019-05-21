"""empty message

Revision ID: c1a3435f800b
Revises: 900fb05fe8c1
Create Date: 2019-05-21 15:50:28.534540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1a3435f800b'
down_revision = '900fb05fe8c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genres_name'), 'genres', ['name'], unique=False)
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
    sa.ForeignKeyConstraint(['GenreId'], ['authors.id'], )
    )
    op.drop_index('ix_genre_name', table_name='genre')
    op.drop_table('genre')
    op.drop_table('BookAuthor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('BookAuthor',
    sa.Column('AuthorId', sa.INTEGER(), nullable=True),
    sa.Column('BookIdooo', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['AuthorId'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['BookIdooo'], ['books.id'], )
    )
    op.create_table('genre',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_genre_name', 'genre', ['name'], unique=False)
    op.drop_table('book_genre')
    op.drop_table('book_author')
    op.drop_index(op.f('ix_genres_name'), table_name='genres')
    op.drop_table('genres')
    # ### end Alembic commands ###
