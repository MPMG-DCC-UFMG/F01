"""empty message

Revision ID: 92c4576a0fd7
Revises: 
Create Date: 2022-08-04 23:13:25.130424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92c4576a0fd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('empresa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('municipio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_ibge', sa.Integer(), nullable=True),
    sa.Column('nome', sa.String(length=30), nullable=False),
    sa.Column('nome_formatado', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('municipioxempresa',
    sa.Column('id_municipio', sa.Integer(), nullable=True),
    sa.Column('id_empresa', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_empresa'], ['empresa.id'], ),
    sa.ForeignKeyConstraint(['id_municipio'], ['municipio.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('municipioxempresa')
    op.drop_table('municipio')
    op.drop_table('empresa')
    # ### end Alembic commands ###
