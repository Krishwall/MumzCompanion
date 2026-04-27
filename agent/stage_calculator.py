from datetime import datetime

def get_stage(date_input: str):
    today = datetime.today()
    try:
        target_date = datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        return "unknown", 0

    days_diff = (target_date - today).days

    if days_diff > 0:
        # Future date -> Pregnancy
        # 40 weeks = 280 days
        weeks_remaining = days_diff // 7
        week = max(1, min(40, 40 - weeks_remaining))
        
        if week <= 13:
            return "early_pregnancy", week
        elif week <= 27:
            return "mid_pregnancy", week
        else:
            return "late_pregnancy", week
    else:
        # Past date -> Postnatal
        days_past = abs(days_diff)
        month = days_past // 30
        
        if month <= 2:
            return "newborn", month
        elif month <= 6:
            return "infant", month
        elif month <= 12:
            return "older_infant", month
        else:
            return "out_of_scope", month