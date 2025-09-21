import uuid
from sqlalchemy import Column, String, Text, Integer, Boolean, JSON, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "app_user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, nullable=False, default="citizen")
    name = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    language = Column(String, default="en")
    consent_json = Column(JSON, default=dict)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    issues = relationship("Issue", back_populates="reporter")

class Issue(Base):
    __tablename__ = "issue"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=False)
    title = Column(Text)
    description = Column(Text, nullable=False)
    category = Column(String)
    status = Column(String, nullable=False, default="new")
    severity = Column(Integer)  # 0..5
    sla_due_at = Column(TIMESTAMP(timezone=True))
    # store lat/lng as int microdegrees for precision without PostGIS in ORM
    lat = Column(Integer)
    lng = Column(Integer)
    address = Column(Text)
    duplicate_group_id = Column(UUID(as_uuid=True))
    public_visibility = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    reporter = relationship("User", back_populates="issues")
    media = relationship("Media", back_populates="issue", cascade="all, delete-orphan")
    actions = relationship("ActionLog", back_populates="issue", cascade="all, delete-orphan")

class Media(Base):
    __tablename__ = "media"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issue.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)  # before|after|extra
    url = Column(Text, nullable=False)
    phash = Column(String)
    exif_json = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    issue = relationship("Issue", back_populates="media")

class ActionLog(Base):
    __tablename__ = "action_log"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issue.id", ondelete="CASCADE"), nullable=False)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id"))
    actor_role = Column(String)
    type = Column(String, nullable=False)  # created|status_change|comment|evidence|reopen_request|system_dedupe
    payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    issue = relationship("Issue", back_populates="actions")
