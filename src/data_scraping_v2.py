import os
from os import system
import re
import numpy as np
import pandas as pd


filepath = "/Users/liangdingli/Projects/Finance_crawler/data/"  # Change path to your own folder path, windos use '\' instead of '/'
title_checklist = {"Filename", "Bankruptcies", "Liens and Judgments", "UCC Filings", "Possible Utility Information", "People at Work", "Address(es) Found", "Possible Properties Owned", "Watercraft", "FAA Certifications", "FAA Aircrafts", "Possible Criminal Records", "Sexual Offenses", "Professional Licenses", "Voter Registration", "Hunting/Fishing Permit", "Concealed Weapons Permit", "Possible Associates", "DEA Controlled Substances", "Possible Relatives", "Neighbors"}
data = [["Filename", "Bankruptcies", "Liens and Judgments", "UCC Filings", "Possible Utility Information", "People at Work", "Address(es) Found", "Possible Properties Owned", "Watercraft", "FAA Certifications", "FAA Aircrafts", "Possible Criminal Records", "Sexual Offenses", "Professional Licenses", "Voter Registration", "Hunting/Fishing Permit", "Concealed Weapons Permit", "Possible Associates", "DEA Controlled Substances", "Possible Relatives", "Neighbors"]]
"""int: Module level variable documented inline.

"""
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
        # print(filename)
        line = fp.readline()
        cur_s = line.strip()
        while cur_s != "Comprehensive Report Summary:" and cur_s != "omprehensive Report Summary:":
            line = fp.readline() #： Don't need the first line "Comprehensive Report Summary:"
            cur_s = line.strip()
        line = fp.readline()
        cnt = 0
        while line != "\n":
            s = line.strip()
            current = ""
            while line != "\n" and s[:-1] not in title_checklist:
                current += ' ' + s
                line = fp.readline()
                s = line.strip()
            if current != "":
                info.append(current.strip())
            line = fp.readline()
            cnt += 1
        if cnt != 21:
            content = fp.read()
            if re.search(r"Possible Utility Information:", content) == None: # Some file without this line
                info.insert(4, "String not found")
                cnt += 1
            if re.search(r"Hunting/Fishing Permit:", content) == None: # Some file without this line
                info.insert(15, "String not found")
                cnt += 1           
        # print(cnt)
        if cnt != 21:
            info.append("") # Some file without neighber content
        return info
    #: Store string into pandas data frame


if __name__ == "__main__":
    for filename in os.listdir(filepath):
        print(filename)
        curr_info = read_txt(filepath, filename)
        print(curr_info)
        print(len(curr_info))
        data.append(curr_info)
    data = np.array(data)
    dataset = pd.DataFrame(data=data[1:, 1:], index=data[1:, 0], columns=data[0, 1:])
    dataset.to_excel("output.xlsx")
    print(data.shape)





