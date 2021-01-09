import os
import pandas as pd

# data folder and template assumed to be in same folder
DATE = "1.6.2020"
DIR = "./Data_" + DATE + "/20210106/"
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
df.to_csv('./Results' + DATE + '.csv', index=False, header=True)
