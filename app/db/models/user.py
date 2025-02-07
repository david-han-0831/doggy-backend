from sqlalchemy import Column, String, Boolean, TIMESTAMP, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class User(Base):
    """ ✅ 사용자 테이블 모델 (Firebase UID 기반) """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firebase_uid = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String(20), nullable=False)

    # 계정 상태 관리
    is_active = Column(Boolean, default=True, nullable=False)
    is_suspended = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    suspended_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # CHECK 제약 조건 추가
    __table_args__ = (
        CheckConstraint(role.in_(['user', 'owner', 'staff', 'superadmin', 'admin_staff']), name="valid_user_role"),
    )
