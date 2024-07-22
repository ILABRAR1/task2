from sqlalchemy.orm import Session
from datetime import timezone
from datetime import datetime
from common.database.models import UserActivity

def log_user_activity(db: Session, username: str, activity: str):
    new_activity = UserActivity(
        username=username,
        activity=activity,
        timestamp=datetime.now()
    )
    db.add(new_activity)
    db.commit()
