"""Initial schema: users, tasks, conversations, messages

Revision ID: 001_initial
Revises:
Create Date: 2025-12-27

This migration creates all 4 required tables per database/schema.md:
1. users (managed by Better Auth)
2. tasks (with user_id for isolation)
3. conversations (stateless chat threads)
4. messages (conversation history for context reconstruction)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables with indexes and constraints."""

    # ==============================================
    # Table 1: users
    # ==============================================
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=False)

    # ==============================================
    # Table 2: tasks
    # ==============================================
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=2000), nullable=True),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('due_time', sa.Time(), nullable=True),
        sa.Column('priority', sa.String(length=10), nullable=False, server_default='medium'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("priority IN ('low', 'medium', 'high')", name='chk_priority'),
        sa.CheckConstraint("status IN ('pending', 'in_progress', 'completed', 'deleted')", name='chk_status')
    )
    # Indexes per database/schema.md
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'], unique=False)
    op.create_index('idx_tasks_status', 'tasks', ['status'], unique=False)
    op.create_index('idx_tasks_priority', 'tasks', ['priority'], unique=False)
    op.create_index('idx_tasks_due_date', 'tasks', ['due_date'], unique=False)
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'], unique=False)
    op.create_index('idx_tasks_user_status', 'tasks', ['user_id', 'status'], unique=False)

    # ==============================================
    # Table 3: conversations
    # ==============================================
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    # Indexes per database/schema.md
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'], unique=False)
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'], unique=False)

    # ==============================================
    # Table 4: messages
    # ==============================================
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='chk_role')
    )
    # Indexes per database/schema.md
    op.create_index('idx_messages_user_id', 'messages', ['user_id'], unique=False)
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'], unique=False)
    op.create_index('idx_messages_created_at', 'messages', ['created_at'], unique=False)
    op.create_index('idx_messages_conv_created', 'messages', ['conversation_id', 'created_at'], unique=False)


def downgrade() -> None:
    """Drop all tables (reverse migration)."""
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('tasks')
    op.drop_table('users')
