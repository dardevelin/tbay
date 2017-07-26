from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey, desc
from sqlalchemy.orm import relationship


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
    
    auction_items = relationship("Item", backref = "seller")
    bids = relationship("Bid", backref = "bidder")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    seller_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    bids = relationship("Bid", backref = "item")
    
class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key = True)
    price = Column(String, nullable = False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

def main():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Harry = User(username="Harry", password="password1")
    David = User(username="David",password="password2")
    Warren = User(username="Warren",password="password3")
    session.add(Harry)
    session.add(David)
    session.add(Warren)
    session.commit()
    
    baseball = Item(name = "baseball", description = "Signed by Madison Bumgarner", seller = Harry)
    session.add(baseball)
    session.commit()
    
    david_bid = Bid(price = 250, user_id = David.id, item = baseball)
    warren_bid = Bid(price = 500, user_id = Warren.id, item = baseball)  

    session.add(david_bid)
    session.add(warren_bid)
    session.commit()
    
    highest_bid = session.query(Bid).order_by(desc(Bid.price)).first()
    
    print("the highest bidder is", highest_bid.bidder.username)

    
main()
