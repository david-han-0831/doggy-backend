import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env 파일 강제 로드
load_dotenv()

class Settings(BaseSettings):
    """
        환경 변수를 관리하는 설정 클래스
    """
    APP_NAME: str = os.getenv("APP_NAME", "Doggy Backend")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")

    # Firebase 설정
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY_ID: str = os.getenv("FIREBASE_PRIVATE_KEY_ID")
    FIREBASE_PRIVATE_KEY: str = os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n')  # Key 값 처리
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL")
    FIREBASE_CLIENT_ID: str = os.getenv("FIREBASE_CLIENT_ID")

    # Supabase 설정
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")
    
    DATABASE_URL: str = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

    
     
    # JWT 설정
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # Redis 설정
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))

    # Pydantic v2 - `Config` 제거 & `model_config`만 사용
    model_config = {
        "env_file": ".env",
        "extra": "allow",  # 불필요한 에러 방지
        "ignored_types": (str,)  # 문자열 타입 필드를 무시
    }
# settings 객체 생성
settings = Settings()
