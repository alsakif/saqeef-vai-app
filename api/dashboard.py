from http.server import BaseHTTPRequestHandler
import json
import os
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    client_id = Column(String(50), nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def handler(event, context):
    session = Session()
    payments = session.query(Payment).all()
    response = [{'id': p.id, 'amount': p.amount, 'client_id': p.client_id} for p in payments]
    session.close()

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }