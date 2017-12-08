"""add live

Revision ID: 0619284b66dd
Revises: aeaf8b5aa724
Create Date: 2017-12-07 16:24:31.083345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0619284b66dd'
down_revision = 'aeaf8b5aa724'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('live',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_live_name'), 'live', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_live_name'), table_name='live')
    op.drop_table('live')
    # ### end Alembic commands ###