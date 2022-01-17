"""empty message

Revision ID: 72e3d4276c56
Revises: 
Create Date: 2022-01-17 17:20:29.146905

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '72e3d4276c56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('infoOrders')
    op.drop_table('rules')
    op.drop_table('schedule')
    op.drop_table('tokens')
    op.drop_table('testuser')
    op.drop_table('winners')
    op.drop_table('products')
    op.drop_table('codes')
    op.drop_table('backets')
    op.drop_table('accounting')
    op.drop_table('address')
    op.drop_table('orders')
    op.drop_table('stock')
    op.drop_table('bonuses')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bonuses',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('idUser', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('dttmUpdate', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['idUser'], ['users.id'], name='bonuses_idUser_fkey'),
    sa.PrimaryKeyConstraint('id', name='bonuses_pkey')
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
    op.create_table('orders',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('dttmAdd', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('idProduct', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('idBacket', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('toping', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['idBacket'], ['backets.id'], name='orders_idBacket_fkey'),
    sa.ForeignKeyConstraint(['idProduct'], ['products.id'], name='orders_idProduct_fkey'),
    sa.PrimaryKeyConstraint('id', name='orders_pkey')
    )
    op.create_table('address',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('idUser', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('floor', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('house', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('intercom', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('apartment', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dttmUpdate', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('entrance', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['idUser'], ['users.id'], name='address_idUser_fkey'),
    sa.PrimaryKeyConstraint('id', name='address_pkey')
    )
    op.create_table('accounting',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('value', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('dttmupdate', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('iduser', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['iduser'], ['testuser.id'], name='accounting_iduser_key'),
    sa.PrimaryKeyConstraint('id', name='accounting_pkey')
    )
    op.create_table('backets',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('backets_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('dttmCreate', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('session', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('idUser', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('option', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dttmClose', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='backets_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('codes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('code', sa.VARCHAR(length=12), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('createAt', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='codes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='codes_pkey')
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
    op.create_table('winners',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('place', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('createAt', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='winners_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='winners_pkey')
    )
    op.create_table('testuser',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('testname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('dttmadd', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='testuser_pkey')
    )
    op.create_table('tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('dttmCreate', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('accessToken', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('idUser', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('dttmExpired', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['idUser'], ['users.id'], name='tokens_idUser_fkey'),
    sa.PrimaryKeyConstraint('id', name='tokens_pkey')
    )
    op.create_table('schedule',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('createAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('dateOpen', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('dateClose', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('reason', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('rule', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('icon', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='schedule_pkey')
    )
    op.create_table('rules',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('productFor', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('productOn', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rule', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('option', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('condition', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='rules_pkey')
    )
    op.create_table('infoOrders',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"infoOrders_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('idAddress', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('dttmCreate', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('idBacket', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('comment', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('appliances', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('pay', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('selfPickup', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('sale', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['idBacket'], ['backets.id'], name='infoOrders_idBacket_fkey'),
    sa.PrimaryKeyConstraint('id', name='infoOrders_pkey')
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
    # ### end Alembic commands ###