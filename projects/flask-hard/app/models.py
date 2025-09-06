from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Literal


class LogRecord(BaseModel):
    timestamp: str
    level: Literal["CRITICAL", "WARNING", "INFO"]
    service: str
    request_id: str
    message: str
    data: Dict[str, Any]

    @validator("timestamp")
    def check_timestamp(cls, v):
        # Basic validation: ensure isoformat-like string (tests provide ISO-like)
        if not isinstance(v, str) or "T" not in v:
            raise ValueError("Invalid timestamp format")
        return v
