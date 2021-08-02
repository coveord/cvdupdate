from threading import Event, Thread

from cvdupdate.cvdupdate import CVDUpdate

# one time per day
WAIT_TIME_SECONDS = 24 * 60 * 60


def start() -> None:
    """Spawns a thread to update the AV db periodically"""
    Thread(target=_update, daemon=True).start()


def _update() -> None:
    """Don't call this directly
    Updates the AV db every day when it was started"""
    ticker = Event()
    m = CVDUpdate()
    while not ticker.wait(WAIT_TIME_SECONDS):
        errors = m.db_update(debug_mode=True)
        if errors > 0:
            m.logger.error(f"Failed to fetch updates from ClamAV databases")
