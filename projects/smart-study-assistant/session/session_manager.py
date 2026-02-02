from typing import List, Dict, Optional
from datetime import datetime


class SessionManager:
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        self.current_session_id = None

    def create_session(self, session_id: Optional[str] = None) -> str:
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.current_session_id = session_id
        return session_id

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })

        if len(self.sessions[session_id]) > self.max_history:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history:]

    def get_history(self, session_id: Optional[str] = None) -> List[Dict[str, str]]:
        session_id = session_id or self.current_session_id

        if session_id and session_id in self.sessions:
            return [
                {'role': msg['role'], 'content': msg['content']}
                for msg in self.sessions[session_id]
            ]

        return []

    def clear_session(self, session_id: Optional[str] = None):
        session_id = session_id or self.current_session_id

        if session_id and session_id in self.sessions:
            self.sessions[session_id] = []

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

        if self.current_session_id == session_id:
            self.current_session_id = None

    def get_session_list(self) -> List[str]:
        return list(self.sessions.keys())

    def set_current_session(self, session_id: str):
        if session_id in self.sessions:
            self.current_session_id = session_id
        else:
            raise ValueError(f"Session {session_id} not found")

    def get_current_session(self) -> Optional[str]:
        return self.current_session_id
