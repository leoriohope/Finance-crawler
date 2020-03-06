import os
from os import system
import re
import numpy as np
import pandas as pd
import csv


filepath = "/Users/liangdingli/Projects/Finance_crawler/data/"  # Change path to your own folder path, windos use '\' instead of '/'
title_checklist = {"Filename", "Bankruptcies", "Liens and Judgments", "UCC Filings", "Possible Utility Information", "People at Work", "Address(es) Found", "Possible Properties Owned", "Watercraft", "FAA Certifications", "FAA Aircrafts", "Possible Criminal Records", "Sexual Offenses", "Professional Licenses", "Voter Registration", "Hunting/Fishing Permit", "Concealed Weapons Permit", "Possible Associates", "DEA Controlled Substances", "Possible Relatives", "Neighbors"}
# data = [["Filename", "Bankruptcies", "Liens and Judgments", "UCC Filings", "Possible Utility Information", "People at Work", "Address(es) Found", "Possible Properties Owned", "Watercraft", "FAA Certifications", "FAA Aircrafts", "Possible Criminal Records", "Sexual Offenses", "Professional Licenses", "Voter Registration", "Hunting/Fishing Permit", "Concealed Weapons Permit", "Possible Associates", "DEA Controlled Substances", "Possible Relatives", "Neighbors"]]
data = []

def read_txt(filepath, filename):
    """Read txt file and clean data, store them into pandas dataframe data type

    Args:
        filepath (string): The first parameter.
        filename (string): The second parameter.
    Returns:
        array : return a 1D array
    """
    #: Read file by line, stop when meet a empty line
    file = filepath + filename
    with open(file) as fp:
        info = [filename]
        #Property
        line = fp.readline()
        while line and line.strip() != "Possible Properties Owned by Subject:Print Possible Properties Owned by Subject Section":
            line = fp.readline() 
        # print("XXXX!")
        while line:
            # line.strip() != "FAA Certifications:Print FAA Certifications Section"
            # print("2")
            cur_list = line.strip().split();
            # if len(cur_list) >= 2 and cur_list[0] == "Property" and (cur_list[1] == "Address:" or cur_list[1] == "Address"):
            #     info.append(' '.join(cur_list[2:]))
            # elif len(cur_list) >= 2 and cur_list[0] == "Sale" and (cur_list[1] == "Price" or cur_list[1] == "Price:"):
            #     info.append(' '.join(cur_list[2:]))
            # elif len(cur_list) >= 2 and cur_list[0] == "Sale" and (cur_list[1] == "Date" or cur_list[1] == "Date:"):
            #     info.append(' '.join(cur_list[2:]))
            if len(cur_list) >= 2 and (cur_list[0] == "Description" or cur_list[0] == "Description:"):
                info.append(' '.join(cur_list[2:]))
            line = fp.readline(); 
        # print(line.strip())
    return info
    #: Store string into pandas data frame


if __name__ == "__main__":
    fileList = os.listdir(filepath)
    fileList.sort(key=lambda x: int(x.split()[0]))
    # print(fileList)

    for filename in fileList:
        print(filename)
        info = read_txt(filepath, filename)
        # print(info)
        data.append(info)
        # print(dta)
    # print(len(data[0]))
    print(max(len(x) for x in data))
    # data.sort(key=lambda x: int(x[0].split()[0]))
    data.insert(0, ["Filename"])
    for i in range(max(len(x) for x in data) - 1):
        data[0].append("Watercarft" + str(i))

    with open("../outputs/out_water.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)





