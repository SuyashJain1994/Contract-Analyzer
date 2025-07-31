web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
release: python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"