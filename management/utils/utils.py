from datetime import datetime

def to_datetime(str_date):
    try:
        return datetime.fromisoformat(str_date[:-5])
    except:
        return None