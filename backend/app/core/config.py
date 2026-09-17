# app/core/config.py
# 설정 담당 = "가게 운영 수첩"
# .env 쪽지에 적힌 값을 읽어와서, 코드 어디서든 꺼내볼 수 있는 수첩으로 정리한다.

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py에서 네 칸 위로 올라가면 kkok/(저장소 루트)이다.
# "server를 어디서 켰는지"와 관계없이 항상 같은 .env를 찾게 해야하기 때문에,
# 현재 폴더가 아니라 config.py 위치를 기준으로 삼는다.
ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """
    수첩의 양식. 여기에 적힌 칸만 .env에서 옮겨 적는다.
    """
    
    model_config = SettingsConfigDict(
        # 쪽지 위치: 저장소 루트의 .env
        env_file=ROOT_DIR / ".env",
        # 한글 주석이 있어도 글자가 깨지지 않게
        env_file_encoding="utf-8",
        # 쪽지에 수첩에 없는 칸(POSTGRES_USER 등)이 있어도 error를 던지지 않고 무시
        extra="ignore",
        # "KEY=" 처럼 빈 칸으로 둔 값은 "적지 않는 것"으로 간주
        env_ignore_empty=True,
    ) 
    
    # DB 창고 주소. 기본값이 없으므로 .env에 없으면 server가 켜지지 않는다.
    # "가게를 차릴 곳이 없으면 가게를 열지 않는 것이 낫다." 
    # 대소문자는 구분하지 않는다. .env의 DATEBASE_URL이 이 곳에 대입된다.
    database_url: str
    
    # JWT_SECRET, REDIS_URL 등은 추후 사용되는 시점에 추가한다.


@lru_cache
def get_settings() -> Settings:
    """
    수첩에 딱 한 번만 적어서 계속 돌려준다.
    
    lru_cache = "한 번 읽은 쪽지는 기억해두기"
    요청이 올 때마다 .env 파일을 다시 열어 읽는 건 비효율적이다.
    수첩에 처음 적었던 내용을 계속 재사용한다.
    """    
    return Settings()
