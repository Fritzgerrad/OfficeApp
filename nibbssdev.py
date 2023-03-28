# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:29:19 2023

@author: fritz
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 00:38:56 2023

@author: fritz
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd


all_my_files = None
CH_DF = None
MC_DF = None
VD_DF = None
LD_DF = None

thedate = ""
MSN=[]
MCHANNEL=[]
MSESSION_ID=[]
MTRANSACTION_TYPE=[]
MRESPONSE=[]
MAMOUNT=[]
MTRANSACTION_TIME=[]
MORIGINATOR_INSTITUTION=[]
MORIGINATOR_BILLER=[]
MDESTINATION_INSTITUTION=[]
MDESTINATION_ACCOUNT_NAME=[]
MDESTINATION_ACCOUNT_NO=[]
MNARRATION=[]
MPAYMENT_REFERENCE=[]
MLAST_12_DIGITS_OF_SESSION_ID=[]

MC = [MSN,MCHANNEL,MSESSION_ID,MTRANSACTION_TYPE,MRESPONSE,MAMOUNT,MTRANSACTION_TIME,MORIGINATOR_INSTITUTION,MORIGINATOR_BILLER,
MDESTINATION_INSTITUTION,MDESTINATION_ACCOUNT_NAME,MDESTINATION_ACCOUNT_NO,MNARRATION,MPAYMENT_REFERENCE,
MLAST_12_DIGITS_OF_SESSION_ID]

 
#Empty lists for Cash234(us) 
CSN=[]
CCHANNEL=[]
CSESSION_ID=[]
CTRANSACTION_TYPE=[]
CRESPONSE=[]
CAMOUNT=[]
CTRANSACTION_TIME=[]
CORIGINATOR_INSTITUTION=[]
CORIGINATOR_BILLER=[]
CDESTINATION_INSTITUTION=[]
CDESTINATION_ACCOUNT_NAME=[]
CDESTINATION_ACCOUNT_NO=[]
CNARRATION=[]
CPAYMENT_REFERENCE=[]
CLAST_12_DIGITS_OF_SESSION_ID=[]

CH = [CSN,CCHANNEL,CSESSION_ID,CTRANSACTION_TYPE,CRESPONSE,CAMOUNT,CTRANSACTION_TIME,CORIGINATOR_INSTITUTION,CORIGINATOR_BILLER,
CDESTINATION_INSTITUTION,CDESTINATION_ACCOUNT_NAME,CDESTINATION_ACCOUNT_NO,CNARRATION,CPAYMENT_REFERENCE,
CLAST_12_DIGITS_OF_SESSION_ID]


#Empty List for Liquid Space
LSN=[]
LCHANNEL=[]
LSESSION_ID=[]
LTRANSACTION_TYPE=[]
LRESPONSE=[]
LAMOUNT=[]
LTRANSACTION_TIME=[]
LORIGINATOR_INSTITUTION=[]
LORIGINATOR_BILLER=[]
LDESTINATION_INSTITUTION=[]
LDESTINATION_ACCOUNT_NAME=[]
LDESTINATION_ACCOUNT_NO=[]
LNARRATION=[]
LPAYMENT_REFERENCE=[]
LLAST_12_DIGITS_OF_SESSION_ID=[]

LD=[LSN,LCHANNEL,LSESSION_ID,LTRANSACTION_TYPE,LRESPONSE,LAMOUNT,LTRANSACTION_TIME,
LORIGINATOR_INSTITUTION,LORIGINATOR_BILLER,LDESTINATION_INSTITUTION,LDESTINATION_ACCOUNT_NAME,
LDESTINATION_ACCOUNT_NO,LNARRATION,LPAYMENT_REFERENCE,LLAST_12_DIGITS_OF_SESSION_ID]


#Empty List Cash234(Mr. Dapo)
VSN=[]
VCHANNEL=[]
VSESSION_ID=[]
VTRANSACTION_TYPE=[]
VRESPONSE=[]
VAMOUNT=[]
VTRANSACTION_TIME=[]
VORIGINATOR_INSTITUTION=[]
VORIGINATOR_BILLER=[]
VDESTINATION_INSTITUTION=[]
VDESTINATION_ACCOUNT_NAME=[]
VDESTINATION_ACCOUNT_NO=[]
VNARRATION=[]
VPAYMENT_REFERENCE=[]
VLAST_12_DIGITS_OF_SESSION_ID=[]

VD = [VSN,VCHANNEL,VSESSION_ID,VTRANSACTION_TYPE,VRESPONSE,VAMOUNT,VTRANSACTION_TIME,
VORIGINATOR_INSTITUTION,VORIGINATOR_BILLER,VDESTINATION_INSTITUTION,VDESTINATION_ACCOUNT_NAME,
VDESTINATION_ACCOUNT_NO,VNARRATION,VPAYMENT_REFERENCE,VLAST_12_DIGITS_OF_SESSION_ID]


def get_lists(df):
    ans = []
    for a in df.columns:
        ans.append(df[a].tolist())
    return ans
        
def clear_lists():
    for lista in MC:
        lista.clear()
    for lista in CH:
        lista.clear()
    for lista in VD:
        lista.clear()
    for lista in LD:
        lista.clear()
        
def get_column(df, col_name):
    for a in df.columns:
        if col_name.upper() in a.upper():
            return df[a].tolist()
        
def put(patner,dflist,dex):
    for i in range(len(dflist)):
        patner[i].append(dflist[i][dex])
        #print("patner lenght is ",len(patner))
        
#def get_input():
 #   input_text = entry.get()
  #  thedate = input_text

def populate_lists(df,day):
    para = get_column(df,"PAYMENT")
    date = get_column(df,"TIME")
    lists = get_lists(df)
    
    for b in range(len(para)):
        if day in str(date[b]):
            #print(str(para[b])[0:3])
            if str(para[b])[0:3] == "'MC":
                put(MC,lists,b)
                     
            elif str(para[b])[0:3] == "'CH":
                put(CH,lists,b)
                
            elif str(para[b])[0:3] == "'VD":
                put(VD,lists,b)
                
            elif str(para[b])[0:3] == "'LD":
                put(LD,lists,b)
            
def save_df(pat,headers):
    df = pd.DataFrame()
    for h in range(len(headers)):
       header = headers[h]
       df[header]=pat[h]
    return df

def get_time(thedate):
    strdate = str(thedate)
    nums = []
    for g in range(10):
        nums.append(str(g))
    number=""
    for h in strdate:
        if h in nums:
            number+=h
    return int(number[8:])

def get_dates(df):
    unique_dates =[]
    all_d = get_column(df,"TIME")
    all_d = [str(t)[1:11] for t in all_d]
    for g in all_d:
        if g not in unique_dates:
            unique_dates.append(g)
    return unique_dates
            
def get_files():
    words_text.delete('1.0', tk.END)
    global all_my_files
    input_file_paths = filedialog.askopenfilenames(
        title="Select a text file",
    filetypes=[("csv files", "*.csv")])
    df_list = []
    for file_path in input_file_paths:
        input_df = pd.read_csv(file_path,encoding='unicode_escape',names=['S/N', 'CHANNEL', 'SESSION ID', 'TRANSACTION TYPE', 'RESPONSE',
       'AMOUNT', 'TRANSACTION TIME', 'ORIGINATOR INSTITUTION',
       'ORIGINATOR / BILLER', 'DESTINATION INSTITUTION',
       'DESTINATION ACCOUNT NAME', 'DESTINATION ACCOUNT NO', 'NARRATION',
       ' PAYMENT REFERENCE', 'LAST 12 DIGITS OF SESSION_ID'])
        #display_count(input_df,thedate,i)  
        df_list.append(input_df)
    
    # concatenate data frames into a single data frame
    df = pd.concat(df_list)
    all_my_files = df
    uniq = get_dates(all_my_files)
    words_text.delete('1.0', tk.END)
    words_text.config(state="normal")
    words_text.insert('1.0',"Available Dates in this report are: ")
    for n in uniq:
        if "20" in n:
            words_text.insert("end","\n")
            words_text.insert('end',n)
    words_text.config(state="disabled")

    
def save_file():
    path_name = filedialog.asksaveasfilename(initialfile= thedate+" NIBSS REPORT.xlsx", defaultextension=".xlsx")
    words_text.config(state="normal")
    
    words_text.insert('end',"\n \n \nWriting to File ...")
    words_text.config(state="disabled")

    with pd.ExcelWriter(path_name) as writer:
        MC_DF.to_excel(writer, sheet_name="MC",index=False)
        CH_DF.to_excel(writer, sheet_name="CH",index=False)
        VD_DF.to_excel(writer, sheet_name="VD",index=False)
        LD_DF.to_excel(writer, sheet_name="LD",index=False)
        
    words_text.config(state="normal")    
    words_text.insert('end',"\n \n \nNIBBS REPORT GENERATED ")
    words_text.config(state="disabled")
    print("DONE")

def get_hour(the_time):
    hour = ""
    hr=""
    the_time = str(the_time)
    first_nums = []
    for g in range(10):
        first_nums.append(str(g))
    hr =  the_time[12:17]
    for p in hr:
        if p in first_nums:
            hour+=p
   # print(hr)

    return int(hour)
    
       
def get_transaction_count(df):
    time_list=[]
    for i in range(4):
        curr_list=[]
        for j in range(6):
            curr_list.append(0)
        time_list.append(curr_list)
    patner_count = get_column(df, "PAYMENT")
    date_check = get_column(df,"TIME")
     
    for k in range(len(patner_count)):
        if "20" in str(date_check[k]):
            curr_time=get_hour(date_check[k])
            #print("curr_time ",str(patner_count[k])[0:3])
            if str(patner_count[k])[0:3] == "'MC":
                #print("boom")
                #time_list[0] = 
                fix_time(curr_time,time_list[0])
                         
            elif str(patner_count[k])[0:3] == "'CH":
                #time_list[1] = 
                fix_time(curr_time,time_list[1])
                
            elif str(patner_count[k])[0:3] == "'VD":
                #time_list[2] = 
                fix_time(curr_time,time_list[2])
                
            elif str(patner_count[k])[0:3] == "'LD":
                #time_list[3] = 
                fix_time(curr_time,time_list[3])
    
    return time_list

def fix_time(actual,super_list):
    print(actual)
    #print(actual)
    if actual > 0 and actual <401:
        super_list[0]+=1
    
    if actual >400 and actual < 801:
        super_list[1]+=1

    if actual > 800 and actual < 1201:
        print(actual)
        super_list[2]+=1

    if actual > 1200 and actual < 1601:
        print(actual)
        super_list[3]+=1

    if actual > 1600 and actual < 2001:
        print(actual)
        super_list[4]+=1

    if actual > 2000 and actual < 2400:
        #print(type(super_list))
       super_list[5]+=1


def display_count(df):
    count = get_transaction_count(df)
    words_text.insert("end" ,"\nMC TRANSACTIONS: ")
    for x in range(len(count[0])):
        words_text.insert("end", '\n')
        words_text.insert("end", str(x+1)+":"+str(count[0][x]))
        words_text.insert("end" ,'\n')

    words_text.insert("end" ,"CH TRANSACTIONS: ")
    for x in range(len(count[1])):
        words_text.insert("end", '\n')
        words_text.insert("end", str(x+1)+":"+str(count[1][x]))
        words_text.insert("end" ,'\n')

    words_text.insert("end" ,"VD TRANSACTIONS: ")
    for x in range(len(count[2])):
        words_text.insert("end" ,'\n')
        words_text.insert("end", str(x+1)+":"+str(count[2][x]))
        words_text.insert("end" ,'\n')

    words_text.insert("end" ,"LD TRANSACTIONS: ")
    for x in range(len(count[3])):
        words_text.insert("end" ,'\n')
        words_text.insert("end", str(x+1)+":"+str(count[3][x]))
        words_text.insert("end", '\n')


# define function to process csv files and create new csv file
def process_csv_files():
    global CH_DF
    global MC_DF
    global VD_DF
    global LD_DF
    global thedate
    thedate=""
    clear_lists()
    # get paths to input csv files
    input_text = entry.get()
    thedate = input_text
    if len(thedate) < 10:
        print ("Please Enter a Valid date")
        words_text.insert('1.0',"Please Enter a Valid date \n")
        return 0
    words_text.config(state="disabled")
    words_text.delete('1.0', tk.END)
    words_text.insert('1.0',"Generating ...")
    words_text.config(state="disabled")

    headers = all_my_files.columns
    populate_lists(all_my_files,thedate)
    CH_DF = save_df(CH,headers)
    MC_DF = save_df(MC, headers)
    VD_DF = save_df(VD,headers)
    LD_DF = save_df(LD,headers)
    
    
    mlen ="MC: "+str(len(MC_DF))
    clen = "CH: "+str(len(CH_DF))
    vlen = "VD: "+str(len(VD_DF))
    llen ="LD: "+str(len(LD_DF))
    
    words_text.config(state="normal")
    words_text.delete('1.0', tk.END)

    words_text.insert('1.0',mlen)
    words_text.insert("end","\n")
    words_text.insert("end","\n")
    words_text.insert('end',clen)
    words_text.insert("end","\n")
    words_text.insert("end","\n")
    words_text.insert('end',vlen)
    words_text.insert("end","\n")
    words_text.insert("end","\n")
    words_text.insert('end',llen)

    display_count(all_my_files)


    words_text.config(state="disabled")


    print(mlen)
    print(clen)
    print(vlen)
    print(llen)
   
   
    
    #label = tk.Label(text = str(len(MC))+str(len(VD)))
    #label.pack()

# create tkinter window
window = tk.Tk()

# add title to window
window.title("GENERATE NIBSS REPORT")
window.geometry('750x500')

# create button to select csv files and process them
files_button = tk.Button(window, text="Select Files", command=get_files)
process_button = tk.Button(window, text="Generate Report", command=process_csv_files)
save_button = tk.Button(window, text="Save", command=save_file)
label = tk.Label(window, text="Select Date")
entry = tk.Entry(window)
words_text = tk.Text(window, height=20, width=50,state="disabled")

# create a button to get the input

 


#button = tk.Button(window, text="Select Date", command=get_input)
#button.pack()

files_button.pack()
entry.pack()
label.pack()   

words_text.pack()
process_button.pack()
save_button.pack()


# run tkinter window
window.mainloop()
