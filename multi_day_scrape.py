from datetime import date, timedelta
from secedgar import DailyFilings
from fake_useragent import UserAgent
import os
import pandas as pd


# per https://sec-edgar.github.io/sec-edgar/filingtypes.html#supported-filing-types
# 'd' represents Regulation D filing

ua = UserAgent()
def get_co(filing_entry):
    return filing_entry.form_type.lower() == "d"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2022, 12, 12)
end_date = date(2022, 12, 13)
for single_date in daterange(start_date, end_date):
    try:
        # form_d = DailyFilings(entry_filter=get_co, date=single_date, user_agent=ua.random)
        # form_d.save('./Data' + single_date.strftime("%m.%d.%Y"))
        DATE = single_date.strftime("%m.%d.%Y")
        DIR = "./Data" + DATE + "/" + single_date.strftime("%Y%m%d") + "/"
        df = pd.read_csv("./EDGAR_Template.csv")

        # global counter for master output file
        df_ctr = 1
        print(os.listdir(DIR))

        # iterate through all instances in a given day
        for folder in os.listdir(DIR):

            # iterate through each file per instance
            for file in os.listdir(DIR + folder):
                file = os.path.join(DIR + folder, file)
                with open(file, 'r') as txt:
                    lines = txt.readlines()
                    try:

                        # check to see if filing is 506(c)
                        tmp, check = lines[6].split('>')
                        if str(check) == "06c\n":

                            # if so, pull the relevant information which is in the first ~50 lines
                            for i in range(4, 50):
                                try:
                                    header, result = lines[i].split(':')
                                    for col in df.columns:

                                        # match each relevant column to available data
                                        if header.lstrip() + ":" == col:
                                            df.loc[df_ctr, col] = result.lstrip()
                                except:
                                    continue

                            # increment global counter, indicating new record
                            df_ctr += 1

                    # represents a 504 offering, different format and irrelevant
                    except:
                        continue

                    # close current file and move to next
                    txt.close()

        # export results of entire day to single csv file
        # df.to_csv('./Results' + DATE + '.csv', index=False, header=True)

    except:
        continue
