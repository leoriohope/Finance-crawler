import os
from os import system
import re
import numpy as np
import pandas as pd
import csv


filepath = "/Users/liangdingli/Projects/Finance_crawler/data/"  # Change path to your own folder path, windos use '\' instead of '/'
title_checklist = {"Filename", "Bankruptcies", "Liens and Judgments", "UCC Filings", "Possible Utility Information", "People at Work", "Address(es) Found", "Possible Properties Owned", "Watercraft", "FAA Certifications", "FAA Aircrafts", "Possible Criminal Records", "Sexual Offenses", "Professional Licenses", "Voter Registration", "Hunting/Fishing Permit", "Concealed Weapons Permit", "Possible Associates", "DEA Controlled Substances", "Possible Relatives", "Neighbors"}
data = [["Filename", "Bankruptcies", "Liens and Judgments", "UCC Filings", "Possible Utility Information", "People at Work", "Address(es) Found", "Possible Properties Owned", "Watercraft", "FAA Certifications", "FAA Aircrafts", "Possible Criminal Records", "Sexual Offenses", "Professional Licenses", "Voter Registration", "Hunting/Fishing Permit", "Concealed Weapons Permit", "Possible Associates", "DEA Controlled Substances", "Possible Relatives", "Neighbors"]]
# data = []
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
        
        
        #Property
        line = fp.readline()
        while line and line.strip() != "Possible Properties Owned by Subject:Print Possible Properties Owned by Subject Section":
            line = fp.readline() 
        # print("XXXX!")
        while line:
            # line.strip() != "FAA Certifications:Print FAA Certifications Section"
            # print("2")
            cur_list = line.strip().split();
            if len(cur_list) >= 2 and cur_list[0] == "Property" and (cur_list[1] == "Address:" or cur_list[1] == "Address"):
                info.append(' '.join(cur_list[3:]))
                line = fp.readline()
                date = False
                price = False
                while line and line.strip() != "Property:":
                    cur_list = line.strip().split()
                    if len(cur_list) >= 2 and cur_list[0] == "Sale" and (cur_list[1] == "Date" or cur_list[1] == "Date:"):
                        info.append(' '.join(cur_list[3:]))
                        date = True
                    if len(cur_list) >= 2 and cur_list[0] == "Sale" and (cur_list[1] == "Price" or cur_list[1] == "Price:"):
                        info.append(' '.join(cur_list[3:]))
                        price = True
                    line  = fp.readline()
                if not price:
                    info.append("Price not found")
                if not date:
                    info.insert(-1, "Date not found")
            


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
    print(len(data[0]))
    print(max(len(x) for x in data))
    # data.sort(key=lambda x: int(x[0].split()[0]))

    for i in range(0, max(len(x) for x in data) - len(data[0]), 3):
        data[0].append("Property" + str(i // 3))
        data[0].append("Date" + str(i // 3))
        data[0].append("Price" + str(i // 3))



    with open("../outputs/out_property.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)





