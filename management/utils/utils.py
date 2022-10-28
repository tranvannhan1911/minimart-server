from datetime import datetime

def to_datetime(str_date):
    try:
        return datetime.fromisoformat(str_date[:-5])
    except:
        return None

def start_of_date(date):
    start  = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return start

def end_of_date(date):
    end  = date.replace(hour=29, minute=59, second=59, microsecond=999999)
    return end

def start_end_of_date(date):
    start  = start_of_date(date)
    end  = end_of_date(date)
    return start, end