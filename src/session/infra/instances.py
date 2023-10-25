from session.infra.shelve_sessions_repository import ShelveSessionsRepository
from session.domain.session_service import SessionService

sessions_repository = ShelveSessionsRepository()
session_service = SessionService(sessions_repository)
