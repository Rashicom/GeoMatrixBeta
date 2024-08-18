from sqlalchemy import Column, DateTime
from datetime import datetime

# model mixins

class TimeStampMixin(object):
    """
    TimeStampMixin
    """
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)