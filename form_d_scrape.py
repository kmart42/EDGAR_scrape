from datetime import date
from secedgar import DailyFilings
from fake_useragent import UserAgent

# per https://sec-edgar.github.io/sec-edgar/filingtypes.html#supported-filing-types
# 'd' represents Regulation D filing

ua = UserAgent()

def get_co(filing_entry):
    return filing_entry.form_type.lower() == "d"


# DailyFilings pulls all filings for a single day
form_d = DailyFilings(entry_filter=get_co, date=date(2021, 1, 6), user_agent=ua.random)
# saved in current directory
form_d.save('./Data_12.26.2022')
