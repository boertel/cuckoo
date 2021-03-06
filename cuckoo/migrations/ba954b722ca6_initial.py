"""initial

Revision ID: ba954b722ca6
Revises:
Create Date: 2018-03-21 09:15:04.954091

"""
import cuckoo
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ba954b722ca6'
down_revision = None
branch_labels = ('default',)
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('client_id', sa.String(length=64), nullable=False),
    sa.Column('client_secret', sa.String(length=64), nullable=False),
    sa.Column('id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('client_id'),
    sa.UniqueConstraint('client_secret')
    )
    op.create_table('option',
    sa.Column('id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.Column('option_id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('value', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('option_id', 'name', name='unq_option_name')
    )
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('application_api_token',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('application_id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.Column('id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.Column('key', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['application.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('application_id'),
    sa.UniqueConstraint('key')
    )
    op.create_table('identity',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('user_id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.Column('external_id', sa.String(length=64), nullable=False),
    sa.Column('provider', sa.String(length=32), nullable=True),
    sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('scopes', postgresql.ARRAY(sa.String(length=64)), nullable=True),
    sa.Column('id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('external_id'),
    sa.UniqueConstraint('user_id', 'provider', name='unq_identity_user')
    )
    op.create_index(op.f('ix_identity_user_id'), 'identity', ['user_id'], unique=False)
    op.create_table('job',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.Column('params', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('schedule', cuckoo.db.types.schedule.Schedule(astext_type=sa.Text()), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.Column('application_id', cuckoo.db.types.guid.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['application.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_application_id'), 'job', ['application_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_job_application_id'), table_name='job')
    op.drop_table('job')
    op.drop_index(op.f('ix_identity_user_id'), table_name='identity')
    op.drop_table('identity')
    op.drop_table('application_api_token')
    op.drop_table('user')
    op.drop_table('option')
    op.drop_table('application')
    # ### end Alembic commands ###
