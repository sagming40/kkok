# 모든 테이블 설계도가 공통으로 물려받는 "표지"
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    모든 model(테이블 설계도)의 부모 class
    
    앞으로 만들 테이블은 모두 이 Base를 상속받는다.
      class Link(Base):
          __tablename__ = "links"
    
    즉, SQLAlchemy가 자식(model)들을 모두 Base.metadata에 모아준다.
    결과적으로 alembic은 Base.metadata 하나만 보면
    "원하는 테이블 전체 목록"을 알 수 있다. (= 배치도 묶음)      
    """
