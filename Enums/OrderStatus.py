from enum import Enum
class OrderStatus(Enum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"