"""Add charity and donation models.

Revision ID: c7bf94d969dc
Revises: bb4acd631f49
Create Date: 2024-09-28 17:25:50.811574

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7bf94d969dc'
down_revision = 'bb4acd631f49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'charityproject',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=True),
        sa.Column('fully_invested', sa.Boolean(), nullable=True),
        sa.Column('create_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'donation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=True),
        sa.Column('fully_invested', sa.Boolean(), nullable=True),
        sa.Column('create_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('donation')
    op.drop_table('charityproject')
    # ### end Alembic commands ###
