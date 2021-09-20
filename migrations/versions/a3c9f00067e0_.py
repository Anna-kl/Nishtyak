"""empty message

Revision ID: a3c9f00067e0
Revises: ac773aa345f1
Create Date: 2021-09-19 12:53:02.606477

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3c9f00067e0'
down_revision = 'ac773aa345f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('codes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('codes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('code', sa.VARCHAR(length=12), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('createAt', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='codes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='codes_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('public_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dttm_add', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('coupon', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('phone', name='users_phone_key')
    )
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('structure', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('dttm_add', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('sale', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('icon', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('tag', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('weight', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('kilocalories', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('complexity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='products_pkey')
    )
    op.create_table('stock',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('describe', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('dttm_add', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('icon', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('tag', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='stock_pkey')
    )
    # ### end Alembic commands ###
