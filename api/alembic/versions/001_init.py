from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('app_user',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('role', sa.String(), nullable=False, server_default='citizen'),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True, unique=True),
        sa.Column('email', sa.String(), nullable=True, unique=True),
        sa.Column('language', sa.String(), nullable=False, server_default='en'),
        sa.Column('consent_json', sa.JSON(), server_default='{}'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )

    op.create_table('issue',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('reporter_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('app_user.id'), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='new'),
        sa.Column('severity', sa.Integer(), nullable=True),
        sa.Column('sla_due_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('lat', sa.Integer(), nullable=True),
        sa.Column('lng', sa.Integer(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('duplicate_group_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('public_visibility', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_issue_reporter', 'issue', ['reporter_id'])
    op.create_index('ix_issue_status_created', 'issue', ['status', 'created_at'])

    op.create_table('media',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('issue_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('issue.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('phash', sa.String(), nullable=True),
        sa.Column('exif_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_media_issue', 'media', ['issue_id'])

    op.create_table('action_log',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('issue_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('issue.id', ondelete='CASCADE'), nullable=False),
        sa.Column('actor_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('app_user.id'), nullable=True),
        sa.Column('actor_role', sa.String(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_action_issue', 'action_log', ['issue_id'])

def downgrade():
    op.drop_index('ix_action_issue', table_name='action_log')
    op.drop_table('action_log')
    op.drop_index('ix_media_issue', table_name='media')
    op.drop_table('media')
    op.drop_index('ix_issue_status_created', table_name='issue')
    op.drop_index('ix_issue_reporter', table_name='issue')
    op.drop_table('issue')
    op.drop_table('app_user')
