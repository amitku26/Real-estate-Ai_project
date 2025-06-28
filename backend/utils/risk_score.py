def compute_risk_score(flood_zone):
    if flood_zone == 1:
        return 90
    elif flood_zone == 2:
        return 50
    else:
        return 10
