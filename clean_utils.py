import pandas as pd

def to_percent(x):
    """Делаем число 0..100 из строк типа '90', '90%', 90."""
    if pd.isna(x):
        return None
    s = str(x).strip()
    s = s.replace('%', '').strip()
    if s == '':
        return None
    try:
        return float(s)
    except:
        return None

def norm_status(x):
    """Приводим статус посещаемости к одному виду."""
    if pd.isna(x):
        return ''
    return str(x).strip().upper()

def is_present(status):
    """Считаем, что Present и Late = был на занятии."""
    s = norm_status(status)
    return (s == 'PRESENT') or (s == 'LATE')
