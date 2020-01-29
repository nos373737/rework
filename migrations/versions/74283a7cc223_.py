"""empty message

Revision ID: 74283a7cc223
Revises: 
Create Date: 2020-01-28 10:31:50.026396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74283a7cc223'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'operator_zone', type_='foreignkey')
    op.drop_column('operator_zone', 'defect_position_id')
    op.drop_column('operator_zone', 'defect_position')
    op.alter_column('out', 'employee_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('out', 'employee_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('operator_zone', sa.Column('defect_position', sa.VARCHAR(length=250), nullable=True))
    op.add_column('operator_zone', sa.Column('defect_position_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key(None, 'operator_zone', 'defect_position', ['defect_position_id'], ['id'])
    # ### end Alembic commands ###