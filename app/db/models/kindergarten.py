from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base
import uuid
import datetime

Base = declarative_base()

class Kindergarten(Base):
    """유치원 정보를 저장하는 데이터베이스 모델"""
    __tablename__ = "kindergartens"

    # 기본 식별자
    id = Column(PG_UUID, primary_key=True, default=uuid.uuid4)
    # 유치원 소유자(원장) ID (users 테이블 참조)
    owner_id = Column(PG_UUID, ForeignKey("users.id"), nullable=False)
    # 유치원 이름
    name = Column(String, nullable=False)
    # 사업자 등록 번호
    business_number = Column(String, unique=True, nullable=False)
    # 유치원 유형 (공립/사립 등)
    type = Column(String, nullable=False)
    # 유치원 주소
    address = Column(String, nullable=False)
    # 연락처
    contact = Column(String, nullable=False)
    # 이메일 주소
    email = Column(String, nullable=False)

    # 인증 상태
    certificate_status = Column(String, nullable=False)
    
    # 계정 상태 관련 필드
    is_active = Column(Boolean, default=True, nullable=False)     # 활성화 상태
    is_suspended = Column(Boolean, default=False, nullable=False)  # 정지 상태
    is_deleted = Column(Boolean, default=False, nullable=False)    # 삭제 상태
    suspended_at = Column(TIMESTAMP, nullable=True)               # 계정 정지 일시
    deleted_at = Column(TIMESTAMP, nullable=True)                 # 계정 삭제 일시

    # 생성 일시
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
