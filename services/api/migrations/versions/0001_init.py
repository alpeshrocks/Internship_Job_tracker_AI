from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('jobs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job_uid', sa.String, nullable=False, unique=True, index=True),
        sa.Column('source', sa.String, nullable=False, index=True),
        sa.Column('title', sa.String, nullable=False, index=True),
        sa.Column('company', sa.String, nullable=False, index=True),
        sa.Column('location', sa.String),
        sa.Column('employment_type', sa.String),
        sa.Column('remote_ok', sa.Boolean),
        sa.Column('visa_friendly', sa.Boolean),
        sa.Column('posted_date', sa.DateTime),
        sa.Column('scraped_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('link', sa.String, nullable=False),
        sa.Column('skills', sa.Text),
        sa.Column('description', sa.Text)
    )
    op.create_index('idx_jobs_posted', 'jobs', ['posted_date'])
    op.create_table('applications',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job_id', sa.Integer, nullable=False, index=True),
        sa.Column('applied', sa.Boolean, server_default=sa.text('FALSE')),
        sa.Column('saved', sa.Boolean, server_default=sa.text('FALSE')),
        sa.Column('notes', sa.Text),
        sa.Column('cold_email_sent', sa.Boolean, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()'))
    )
    op.create_index('idx_app_job', 'applications', ['job_id'])
    op.create_table('embeddings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kind', sa.String, index=True),
        sa.Column('ref_id', sa.Integer, index=True),
        sa.Column('dim', sa.Integer),
        sa.Column('vec', sa.LargeBinary)
    )

def downgrade():
    op.drop_table('embeddings')
    op.drop_index('idx_app_job', table_name='applications')
    op.drop_table('applications')
    op.drop_index('idx_jobs_posted', table_name='jobs')
    op.drop_table('jobs')
