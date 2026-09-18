# alembic이 자동 생성(autogenerate)을 할때, 테이블 설계도들이 "Python에 loading 되어 있어야" 감지된다.
# new model 파일을 생성하면 backend\app\modes\__init__.py에 import를 한줄 씩 추가한다.
# ⚠️ import를 빠뜨리면 alembic이 그 테이블을 "존재하지 않는" 것으로 간주하고 Delete Migration을 생성한다. ⚠️
from app.models.base import Base

__all__ = ["Base"]
