from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
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
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method not allowed'})
        }

    body = json.loads(event['body'])
    amount = body.get('amount')
    client_id = body.get('client_id')

    if not amount or not client_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing amount or client_id'})
        }

    session = Session()
    payment = Payment(amount=amount, client_id=client_id)
    session.add(payment)
    session.commit()

    response = {
        'message': 'Payment added',
        'payment': {'id': payment.id, 'amount': payment.amount, 'client_id': payment.client_id}
    }
    session.close()

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }