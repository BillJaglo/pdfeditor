

def calculate_usd_total(usd_string):
    usd_value_float = round(float(usd_string.replace(',', '')), 2)
    # takes the invoice usd value discounted at the .98 rate and finds the full value, turns it into a float
    full_usd_amount = usd_value_float / 0.98
    # rounds the float number to 2 decimal places
    full_usd_amount_rounded = round(full_usd_amount, 2)
    return full_usd_amount_rounded


def calculate_commission_total(full_usd_rounded, usd_string):
    usd_value_float = round(float(usd_string.replace(',', '')), 2)
    return round(full_usd_rounded - usd_value_float, 2) * -1

