

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional


@dataclass
class HttpSessionField:
    user_id: int
    expires_at: datetime

class HttpSession:
    def __init__(self) -> None:
        self._sessions: Dict[str, HttpSessionField] = {}
        self._lock = asyncio.Lock()
    
    async def set(self, session_id: str, user_id: int, ttl_minutes: int):
        async with self._lock:
           self._sessions[session_id] = HttpSessionField(
                user_id=user_id,
                expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes),
           )

    async def get(self, session_id: str) -> Optional[int]:
        async with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return None
            
            if session.expires_at < datetime.utcnow():
                del self._sessions[session_id]
                return None
            
            return session.user_id
            
    async def invalidate(self, session_id: str):
        async with self._lock:
            self._sessions.pop(session_id, None)


http_session = HttpSession()