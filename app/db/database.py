from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.utils.config import settings  # 설정 불러오기
from sqlalchemy.ext.declarative import declarative_base


# Load environment variables from .env
load_dotenv()

# Construct the SQLAlchemy connection string
DATABASE_URL = settings.DATABASE_URL

Base = declarative_base()

# SQLAlchemy 엔진 생성 (Transaction Pooler 사용 시, Pooling 해제)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 세션을 관리하는 의존성 함수
def get_db():
    """
    FastAPI 엔드포인트에서 사용할 데이터베이스 세션을 반환하는 함수.
    요청이 끝나면 세션을 자동으로 닫음.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
