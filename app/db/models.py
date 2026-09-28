from datetime import datetime

from sqlalchemy import Integer, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class RunLog(Base):

    __tablename__ = "run_logs"

    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    node_name = Column(String)
    input_data = Column(Text)
    output_data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)



class EvalResult(Base):
    __tablename__ = "eval_results"

    id = Column(Integer, primary_key=True)
    eval_run_id = Column(String, index=True)    
    query_id = Column(String)                    
    query = Column(Text)
    run_id = Column(String)                      
    passed = Column(String)                      
    details = Column(Text)                       
    created_at = Column(DateTime, default=datetime.utcnow)