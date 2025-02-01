from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base
import uuid
import datetime

Base = declarative_base()

class User(Base):
    """사용자 정보를 저장하는 데이터베이스 모델"""
    __tablename__ = "users"

    # 기본 식별자
    id = Column(PG_UUID, primary_key=True, default=uuid.uuid4)
    # Firebase 인증 고유 ID
    firebase_uid = Column(String, unique=True, nullable=False)
    # 사용자 이메일
    email = Column(String, unique=True, nullable=False)
    # 사용자 역할 (권한)
    role = Column(String, nullable=False)

    # 계정 상태 관련 필드
    is_active = Column(Boolean, default=True, nullable=False)     # 활성화 상태
    is_suspended = Column(Boolean, default=False, nullable=False)  # 정지 상태
    is_deleted = Column(Boolean, default=False, nullable=False)    # 삭제 상태
    suspended_at = Column(TIMESTAMP, nullable=True)               # 계정 정지 일시
    deleted_at = Column(TIMESTAMP, nullable=True)                 # 계정 삭제 일시

    # 생성 일시
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
