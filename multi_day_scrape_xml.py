from datetime import date, timedelta
from secedgar import DailyFilings
from fake_useragent import UserAgent
from tkinter import *
from tkinter import ttk
import os
import pandas as pd


# per https://sec-edgar.github.io/sec-edgar/filingtypes.html#supported-filing-types
# 'd' represents Regulation D filing

ua = UserAgent()
win = Tk()


def get_co(filing_entry):
    return filing_entry.form_type.lower() == "d"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def process():
    global s_year
    global s_month
    global s_day
    global e_year
    global e_month
    global e_day
    global lbl

    start_date = date(int(s_year.get()), int(s_month.get()), int(s_day.get()))
    end_date = date(int(e_year.get()), int(e_month.get()), int(e_day.get()))
    lbl = Label(win, text="Running...")
    lbl.pack()
    lbl.update()

    for single_date in daterange(start_date, end_date):
        try:
            form_d = DailyFilings(entry_filter=get_co, date=single_date, user_agent=ua.random)
            form_d.save('./Data' + single_date.strftime("%m.%d.%Y"))
            DATE = single_date.strftime("%m.%d.%Y")
            DIR = "./Data" + DATE + "/" + single_date.strftime("%Y%m%d") + "/"
            df = pd.read_csv("./EDGAR_Template.csv")

            # global counter for master output file
            df_ctr = 1

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
                                i = 1
                                while i < len(lines):
                                    if "COMPANY CONFORMED NAME:" in lines[i]:
                                        tmp, co_name = lines[i].split(":")
                                    if "<relatedPersonsList>" in lines[i]:
                                        while "</relatedPersonsList>" not in lines[i]:
                                            if "<relatedPersonInfo>" in lines[i]:
                                                while "</relatedPersonInfo>" not in lines[i]:
                                                    header = lines[i][lines[i].find("<") + 1:lines[i].find(">")]
                                                    for col in df.columns:
                                                        if header == col:
                                                            result = lines[i][lines[i].find(">") + 1:lines[i].rfind("</")]
                                                            df.loc[df_ctr, col] = result
                                                    i+=1
                                                df_ctr += 1
                                            i+=1
                                    header = lines[i][lines[i].find("<") + 1:lines[i].find(">")]
                                    for col in df.columns:
                                        if header == col:
                                            result = lines[i][lines[i].find(">") + 1:lines[i].rfind("</")]
                                            df.loc[df_ctr, col] = result
                                    i += 1
                                df_ctr += 1
                                    # try:
                                    #     header, result = line.split(':')
                                    #     for col in df.columns:
                                    #
                                    #         # match each relevant column to available data
                                    #         if header.lstrip() + ":" == col:
                                    #             df.loc[df_ctr, col] = result.lstrip()
                                    # except:
                                    #     continue

                                # increment global counter, indicating new record

                        # represents a 504 offering, different format and irrelevant
                        except:
                            continue

                        # close current file and move to next
                        txt.close()

            # export results of entire day to single csv file
            df.to_csv('./New_Results' + DATE + '.csv', index=False, header=True)

        except:
            continue
    win.destroy()



# start_date = date(2022, 12, 12)
# end_date = date(2022, 12, 13)

today = date.today()

#Create an Entry widget to accept User Input
beg = Label(win, text="Start Date")
beg.pack()

s_year= Entry(win, width= 40)
s_year.insert(0, str(today.year))
s_year.focus_set()
s_year.pack()

s_month= Entry(win, width= 40)
s_month.insert(0, str(today.month))
s_month.focus_set()
s_month.pack()

s_day= Entry(win, width= 40)
s_day.insert(0, str(today.day - 1))
s_day.focus_set()
s_day.pack()

end = Label(win, text="End Date")
end.pack()

e_year= Entry(win, width= 40)
e_year.insert(0, str(today.year))
e_year.focus_set()
e_year.pack()

e_month= Entry(win, width= 40)
e_month.insert(0, str(today.month))
e_month.focus_set()
e_month.pack()

e_day= Entry(win, width= 40)
e_day.insert(0, str(today.day))
e_day.focus_set()
e_day.pack()

#Create a Button to validate Entry Widget
btn = Button(win, text="Run",width= 20, command=process)
btn.pack()

lbl = Label(win, text="Click to Start")
lbl.pack()


win.mainloop()