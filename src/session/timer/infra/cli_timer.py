from session.timer.domain.timer_observer import TimerObserver

class CLITimer(TimerObserver):
    def update(self, new_time_minutes: int, new_time_seconds: int) -> None:
        print(f'{new_time_minutes:00}:{new_time_seconds:00}')
