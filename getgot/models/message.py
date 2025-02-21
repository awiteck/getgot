# src/getgot/models/message.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class Message(BaseModel):
    content: str
    role: str  # e.g. "user", "assistant"
    timestamp: datetime
    metadata: Optional[Dict[Any, Any]] = None
