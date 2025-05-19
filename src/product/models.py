from sqlalchemy import Column, String, Uuid, ForeignKey, Float, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Uuid, primary_key=True)
    client_id = Column(Uuid, ForeignKey('clients.id'), nullable=False)
    product_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    image = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    review_score = Column(Float)
    
    # client = relationship("Client", back_populates="favorites")
    
    # __table_args__ = (
    #     {'sqlite_autoincrement': True},
    #     {'unique_constraint': ['client_id', 'product_id']}
    # )
