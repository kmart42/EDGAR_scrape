from datetime import date
from secedgar.filings import DailyFilings


# per https://sec-edgar.github.io/sec-edgar/filingtypes.html#supported-filing-types
# 'd' represents Regulation D filing
def get_co(filing_entry):
    return filing_entry.form_type.lower() == "d"


# DailyFilings pulls all filings for a single day
form_d = DailyFilings(entry_filter=get_co, date=date(2021, 1, 6))
# saved in current directory
form_d.save('./Data_1.6.2020')
