from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


def _check_db(engine: Engine, retries=5, interval=1.0):
  last_err = None
  for _ in range(retries):
    try:
      with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
      return True
    except Exception as e:
      last_err = e
      import time

      time.sleep(interval)
  raise RuntimeError(f"DB health check failed: {last_err}")


class DatabaseManager:
  def __init__(self):
    self.engine = None
    self.SessionLocal = None

  def init(self, uri: str):
    self.engine = create_engine(
      uri, pool_pre_ping=True, pool_size=5, max_overflow=10, pool_timeout=5
    )
    _check_db(self.engine)
    self.SessionLocal = sessionmaker(bind=self.engine)

  def get_session(self) -> Session:
    if self.SessionLocal is None:
      raise RuntimeError("DatabaseManager not init")
    return self.SessionLocal()
