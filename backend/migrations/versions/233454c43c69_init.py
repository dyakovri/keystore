"""Init

Revision ID: 233454c43c69
Revises: 
Create Date: 2023-09-24 17:05:14.484055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '233454c43c69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'secret',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('create_ts', sa.DateTime(), nullable=False),
        sa.Column('update_ts', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'secret_key',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('secret', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'secret_owners',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('secret_id', sa.UUID(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('access', sa.Enum('OWNER', 'RW', 'R', name='access', native_enum=False), nullable=False),
        sa.ForeignKeyConstraint(
            ['secret_id'],
            ['secret.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'version',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('secret_id', sa.UUID(), nullable=False),
        sa.Column('num', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('value', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(
            ['secret_id'],
            ['secret.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('version')
    op.drop_table('secret_owners')
    op.drop_table('secret_key')
    op.drop_table('secret')
    # ### end Alembic commands ###
