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
import os
import zipfile

agent_managers = None
all_my_files = None
all_my_files_failed = None 
FT=[]
CS=[]
file_times = {}
file_times_failed ={}
comm_df = pd.DataFrame()
df_funds = pd.DataFrame()
df_cash=pd.DataFrame()

CH_DF = None
MC_DF = None
VD_DF = None
LD_DF = None

CH_DFF = None
MC_DFF = None
VD_DFF = None
LD_DFF = None

thedate = ""
thedatefailed=''

FAILED = []
for i in range(4):
    comp = []
    for j in range(15):
        colu =[]
        comp.append(colu)
    FAILED.append(comp)
    
SUCC = []
for i in range(4):
    comp = []
    for j in range(15):
        colu =[]
        comp.append(colu)
    SUCC.append(comp)
    
 
def get_lists(df):
    ans = []
    for a in df.columns:
        ans.append(df[a].tolist())
    return ans
        
        
def get_index(word,ch):
    for x in word:
        if word[x] == ch:
            return x
        
        
def clear_lists( sup):
    
    for f in sup:
        for d in f:
            d.clear()
       
        
def get_column(df, col_name):
    for a in df.columns:
        if col_name.upper() in a.upper():
            return df[a].tolist()
   
        
def put(patner,dflist,dex):
    for i in range(len(dflist)):
        patner[i].append(dflist[i][dex])
        

def populate_lists(df,out,day):
    para = get_column(df,"PAYMENT")
    date = get_column(df,"TIME")
    lists = get_lists(df)
    if day == "All Available Dates":
        for b in range(len(para)):
            if str(para[b])[0:3] == "'MC":
                put(out[0],lists,b)
                     
            elif str(para[b])[0:3] == "'CH":
                put(out[1],lists,b)
                
            elif str(para[b])[0:3] == "'VD":
                put(out[2],lists,b)
                
            elif str(para[b])[0:3] == "'LD":
                put(out[3],lists,b)
        
    else:
        for b in range(len(para)):
            if day in str(date[b]):
                if str(para[b])[0:3] == "'MC":
                    put(out[0],lists,b)
                        
                elif str(para[b])[0:3] == "'CH":
                    put(out[1],lists,b)
                    
                elif str(para[b])[0:3] == "'VD":
                    put(out[2],lists,b)
                    
                elif str(para[b])[0:3] == "'LD":
                    put(out[3],lists,b)
                     
            
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
            
  
def get_all_files():
    global all_my_files
    global all_my_files_failed
    global file_times
    global file_times_failed
    
    words_text.config(state="normal")
    words_text_failed.config(state="normal")
    
    
    words_text_failed.delete('1.0', tk.END)
    words_text.delete('1.0', tk.END)
    date_list_succ.delete(0,tk.END)
    date_list_failed.delete(0,tk.END)
    
    file_times={}
    file_times_failed={}
    
    succ = "NIP_894_outwards successful.csv"
    unsucc = "NIP_894_outwards unsuccessful.csv"
    directory = filedialog.askdirectory()
    df_list = get_csv_from_directory(directory, succ)
    df_list_failed = get_csv_from_directory(directory, unsucc)
    
    df = pd.concat(df_list)
    df_failed = pd.concat(df_list_failed)
            
    all_my_files = df
    all_my_files_failed = df_failed
    uniq = get_dates(all_my_files)
    uniq_failed = get_dates(all_my_files_failed)
    words_text_failed.delete('1.0', tk.END)
    words_text.delete('1.0', tk.END)
    
    
    label_succ.config(text="Successful Transactions:                                    ")
    label_failed.config(text="Failed Transactions: ")

    for n in uniq:
        if "20" in n:
            date_list_succ.insert(tk.END,n)
    date_list_succ.insert(tk.END,"All Available Dates")
    words_text.config(state="disabled")
    
    for n in uniq_failed:
        if "20" in n:
            date_list_failed.insert(tk.END,n)
    date_list_failed.insert(tk.END,"All Available Dates")
    words_text_failed.config(state="normal")
    
    words_text.config(state="normal")
    words_text.insert(tk.END,"Date Ranges for the report are: \n\n")
    words_text_failed.insert(tk.END,"Date Ranges for the report are: \n\n")
        
    file_times = dict(sorted(file_times.items()))
    file_times_failed= dict(sorted(file_times_failed.items()))

    for d in file_times:
        a = file_times[d][0]
        amt = get_range_amount(a)
        dat = get_report_range(a)
        words_text.insert(tk.END,d+" >>\n "+str((amt[1]))+"("+str((amt[0]))+")")
        words_text.insert(tk.END,"\n\n")
    
    for d in file_times_failed:
        a = file_times_failed[d][0]
        amt = get_range_amount(a)
        dat = get_report_range(a)
        words_text_failed.insert(tk.END,d+" >>\n "+str((amt[1]))+"("+str((amt[0]))+")")
        words_text_failed.insert(tk.END,"\n\n")
    
    
    words_text_failed.config(state="disabled")
    words_text.config(state="disabled")


def get_zip(zip_file, contains_string):
     
    dataframe_list = []
    with zipfile.ZipFile(zip_file, 'r') as zfile:
        zfile.extractall()
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                if name.endswith('.csv') and contains_string in name:
                    df = pd.read_csv(file_path,encoding='unicode_escape',names=['S/N', 'CHANNEL', 'SESSION ID', 'TRANSACTION TYPE', 'RESPONSE',
                    'AMOUNT', 'TRANSACTION TIME', 'ORIGINATOR INSTITUTION',
                    'ORIGINATOR / BILLER', 'DESTINATION INSTITUTION',
                    'DESTINATION ACCOUNT NAME', 'DESTINATION ACCOUNT NO', 'NARRATION',
                    ' PAYMENT REFERENCE', 'LAST 12 DIGITS OF SESSION_ID'])
                        #display_count(input_df,thedate,i)  
                    dataframe_list.append(df)
                    os.remove(file_path)
                elif name.endswith('.csv') or name.endswith('.txt') or name.endswith('.pdf'):
                    os.remove(file_path) # delete the processed zip file        
    return dataframe_list


def get_csv_from_directory(directory, contains_string):
    global file_times
    global file_times_failed
    dataframe_list = []
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            if name.endswith('.csv') and contains_string in name:
                file_path = os.path.join(root, name)
                df = pd.read_csv(file_path)
                dataframe_list.append(df)
            elif name.endswith('.zip'):
                file_path = os.path.join(root, name)                 
                zip_dataframes = get_zip(file_path, contains_string)
                dataframe_list += zip_dataframes
                if not "unsuccessful" in contains_string:
                    file_times[name[52:63]] = zip_dataframes
                else:
                    file_times_failed[name[52:63]] = zip_dataframes
                    
                
    return dataframe_list

 
def save_succ_file():
    path_name = filedialog.asksaveasfilename(initialfile= thedate+" NIBSS SUCCSSFUL REPORT.xlsx", defaultextension=".xlsx")
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


def save_failed_file():
    path_name = filedialog.asksaveasfilename(initialfile= thedate+" NIBSS FAILED REPORT.xlsx", defaultextension=".xlsx")
    words_text_failed.config(state="normal")
    
    words_text_failed.insert('end',"\n \n \nWriting to File ...")
    words_text_failed.config(state="disabled")

    with pd.ExcelWriter(path_name) as writer:
        MC_DFF.to_excel(writer, sheet_name="MC",index=False)
        CH_DFF.to_excel(writer, sheet_name="CH",index=False)
        VD_DFF.to_excel(writer, sheet_name="VD",index=False)
        LD_DFF.to_excel(writer, sheet_name="LD",index=False)
        
    words_text_failed.config(state="normal")    
    words_text_failed.insert('end',"\n \n \nNIBBS REPORT GENERATED ")
    words_text_failed.config(state="disabled")
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
    #print(actual)
    if actual > 0 and actual <401:
        super_list[0]+=1
    
    if actual >400 and actual < 801:
        super_list[1]+=1

    if actual > 800 and actual < 1201:
        super_list[2]+=1

    if actual > 1200 and actual < 1601:
        super_list[3]+=1

    if actual > 1600 and actual < 2001:
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
def process_csv_succ_files():
    global CH_DF
    global MC_DF
    global VD_DF
    global LD_DF
    global SUCC
    global thedate
    thedate=""
    clear_lists(SUCC)
    #thedate = input_text
    thedate = date_list_succ.get(tk.ACTIVE)
    
    if len(thedate) < 10:
        print ("Please Enter a Valid date")
        words_text.insert('1.0',"Please Enter a Valid date \n")
        return 0
    words_text.config(state="disabled")
    words_text.delete('1.0', tk.END)
    words_text.insert('1.0',"Generating ...")
    words_text.config(state="disabled")
    headers = all_my_files.columns
    populate_lists(all_my_files,SUCC,thedate)
 
    MC_DF = save_df(SUCC[0], headers)
    CH_DF = save_df(SUCC[1],headers)
    VD_DF = save_df(SUCC[2],headers)
    LD_DF = save_df(SUCC[3],headers)
    
    mcash_amount = MC_DF["AMOUNT"]
    mcash_amount = [float(a) for a in mcash_amount]
    ch_amount = CH_DF["AMOUNT"]
    ch_amount = [float(a) for a in ch_amount]
    vd_amount = VD_DF["AMOUNT"]
    vd_amount = [float(a) for a in vd_amount]
    ld_amount = LD_DF["AMOUNT"]
    ld_amount = [float(a) for a in ld_amount]
  
    
    mlen ="MC: "+str(len(MC_DF))+" ("+str(sum(mcash_amount))+")"
    clen = "CH: "+str(len(CH_DF))+" ("+str(sum(ch_amount))+")"
    vlen = "VD: "+str(len(VD_DF))+" ("+str(sum(vd_amount))+")"
    llen ="LD: "+str(len(LD_DF))+"("+str(sum(ld_amount))+")"
    
    words_text.config(state="normal")
    words_text.delete('1.0', tk.END)
    words_text.insert('1.0',mlen)
    words_text.insert("end","\n")
    words_text.insert('end',clen)
    words_text.insert("end","\n")
    words_text.insert('end',vlen)
    words_text.insert("end","\n")
    words_text.insert('end',llen)

    #display_count(all_my_files)


    words_text.config(state="disabled")


    print(mlen)
    print(clen)
    print(vlen)
    print(llen)
   
   
def process_csv_unsucc_files():
    global CH_DFF
    global MC_DFF
    global VD_DFF
    global LD_DFF
    global FAILED
    global thedatefailed
 
    clear_lists(FAILED)
    words_text_failed.delete('1.0', tk.END)
    thedatefailed = date_list_failed.get(tk.ACTIVE)
    if len(thedatefailed) < 10:
        words_text_failed.insert('1.0',"There are no failed transactions in this report \n")
        return 0
    words_text_failed.config(state="disabled")
    words_text_failed.delete('1.0', tk.END)
    words_text_failed.insert('1.0',"Generating ...")
    words_text_failed.config(state="disabled")
    headers = all_my_files_failed.columns
    
    populate_lists(all_my_files_failed,FAILED,thedatefailed)
   
    MC_DFF = save_df(FAILED[0], headers)
    CH_DFF = save_df(FAILED[1],headers)
    VD_DFF = save_df(FAILED[2],headers)
    LD_DFF = save_df(FAILED[3],headers)
   
    
    mcash_amount = MC_DFF["AMOUNT"]
    mcash_amount = [float(a) for a in mcash_amount]
    ch_amount = CH_DFF["AMOUNT"]
    ch_amount = [float(a) for a in ch_amount]
    vd_amount = VD_DFF["AMOUNT"]
    vd_amount = [float(a) for a in vd_amount]
    ld_amount = LD_DFF["AMOUNT"]
    ld_amount = [float(a) for a in ld_amount]
  
    
    mlen ="MC: "+str(len(MC_DFF))+" ("+str(sum(mcash_amount))+")"
    clen = "CH: "+str(len(CH_DFF))+" ("+str(sum(ch_amount))+")"
    vlen = "VD: "+str(len(VD_DFF))+" ("+str(sum(vd_amount))+")"
    llen ="LD: "+str(len(LD_DFF))+"("+str(sum(ld_amount))+")"
    
    words_text_failed.config(state="normal")
    words_text_failed.delete('1.0', tk.END)
    words_text_failed.insert('1.0',mlen)
    words_text_failed.insert("end","\n")
    words_text_failed.insert('end',clen)
    words_text_failed.insert("end","\n")
    words_text_failed.insert('end',vlen)
    words_text_failed.insert("end","\n")
    words_text_failed.insert('end',llen)

    #display_count(all_my_files)

    words_text_failed.config(state="disabled")

    print(mlen)
    print(clen)
    print(vlen)
    print(llen)
    
    
def make_int(the_list):
    ans = []
    numrals=[1,2,3,4,5,6,7,8,9,0]
    for num in the_list:
        curr = ""
        for a in str(num):
            if a in numrals:
                curr+=a
        if len(curr) > 0:
            ans.append(curr)
    ans = [int(a) for a in ans]
    return ans
    
    
def get_cs_commision(the_list):
    for i in range(len(the_list)):
        if the_list[i] < 100:
            the_list[i] = 0
        
        elif the_list[i] > 99 and the_list[i] < 1500:
            the_list[i] = 0.1
        
        elif the_list[i] > 1499.99 and the_list[i] < 3000:
            the_list[i] = 0.3
        
        elif the_list[i] > 2999.9 and the_list[i] < 8000:
            the_list[i] = 1.0
        
        elif the_list[i] > 7999.99 and the_list[i] < 15000:
            the_list[i] = 3.0
        
        elif the_list[i] > 14999.99:
            the_list[i] = 5
    
    return the_list    


def get_ft_transactions():
    global FT
    funds = filedialog.askopenfile()
    df_funds = pd.read_csv(funds,encoding='unicode_escape')
    FT.append(df_funds['Agents'].tolist())
    FT.append(df_funds['Agent Managers'].tolist())
    FT.append(df_funds['Amount'].tolist())
    comms_text.insert(tk.END,"TOTAL FUNDS TRANSFER TRANSACTIONS: "+str(len(FT[0]))+"\n")

    print("FT DONE")
  
  
def get_cash_transactions():
    global CS
    cash = filedialog.askopenfile()
    df_cash = pd.read_csv(cash,encoding='unicode_escape')
    CS.append(df_cash['Agents'].tolist())
    CS.append(df_cash['Agent Managers'].tolist())
    CS.append(df_cash['Amount'].tolist())
    comms_text.insert(tk.END,"TOTAL CASHOUT TRANSACTIONS: "+str(len(CS[0]))+"\n")
    print("CS DONE")


def generate_ft():
    global FT
    ans = {}
    for x in range(len(FT[1])):
        if FT[1][x] in ans:
            ans[FT[1][x]]=ans[FT[1][x]] + 1
            
        else:
            ans[FT[1][x]] = 1

    return ans


def generate_cs():
    global CS
    ans={}

    CS[2] = get_cs_commision(CS[2])
    for x in range(len(CS[0])):
        if CS[1][x] in ans:
            ans[CS[1][x]] = ans[CS[1][x]] + CS[2][x]
            
        else:
             
            ans[CS[1][x]] = CS[2][x]
    
    return ans


def get_total_commision():
    global comm_df
    global CS
    global FT
    global df_cash
    global df_funds
    
    
    comms_text.insert(tk.END,"\n")
    comms_text.insert(tk.END,"\n")
    comms_text.insert(tk.END,"\n")    

    ans = {}
    ft_comm = generate_ft()
    cs_comm = generate_cs()
    k,v = [],[]
    
    for key, value in ft_comm.items():
        k.append(key)
        v.append(value)
    df_funds["Agent Managers"] = k
    df_funds["Commissions"] = v
    
    k1,v1 = [],[]
    
    for key, value in cs_comm.items():
        k1.append(key)
        v1.append(value)
        
    df_cash["Agent Managers"] = k1
    df_cash["Commissions"] = v1
         
    for x in range(len(k)):
        ans[k[x]]=v[x]
        
    for x in range(len(k1)):
        if k1[x] in ans:
            ans[k1[x]] = ans[k1[x]] + v1[x]
            
        else:
            ans[k1[x]] = v1[x]
            
            
    agm_val , his_commision =[],[]       
    for key, value in ans.items():
        agm_val.append(key)
        his_commision.append(value)
        
    
    comm_df["AGENT MANAGER"] = agm_val
    comm_df["COMMISION"] = his_commision
    pd.set_option('display.max_rows', None)  # To display all rows
    pd.set_option('display.max_columns', None) 
    comms_text.insert(tk.END,str(comm_df))
    comms_text.config(state="disabled")
    
    
def save_file_for_commision_generator():
    global comm_df
    global df_funds
    global df_cash
    
    path_name_comm = filedialog.asksaveasfilename(initialfile = "March Agent Manager Commision", defaultextension=".xlsx")

    with pd.ExcelWriter(path_name_comm) as writer:
        df_funds.to_excel(writer, sheet_name="Fund Transfer Commisions",index=False)
        df_cash.to_excel(writer, sheet_name="Cash Out Commisions",index=False)
        comm_df.to_excel(writer, sheet_name="Total Commisions",index=False)
  
                
def get_report_range(df):
    dates = []
    this_dates = get_column(df,"TIME")
    for c in this_dates:
        if "20" in str(c):
            dates.append(c)

    return str(dates[0])[6:17]+" to "+str(dates[len(dates)-1])[6:17]


def get_range_amount1(df):
    total = 0
    count = 0
    this_amount = get_column(df,"AMOUNT")
    this_ref = get_column(df,"PAYMENT")
    for b in range(len(this_amount)):
        pal  = str(this_ref[b])[0:3]
        if pal  =="'MC" or pal == "'CH" or pal == "'VD" or pal == "'LD":
            total+= float(this_amount[b])
            count+=1
    print("in",len(this_amount),"out",count)
    return [total,count]

def currency(mt):
    return "N" + "{:,.2f}".format(mt)

def get_range_amount(df):
    total = 0
    count = 0
    amount = get_column(df,"AMOUNT")
    para = get_column(df,"PAYMENT")
    for b in range(len(para)):
        if str(para[b])[0:3] == "'MC":
            total+=float(amount[b])
            count+=1
                     
        elif str(para[b])[0:3] == "'CH":
            total+=float(amount[b])
            count+=1
            
        elif str(para[b])[0:3] == "'VD":
            total+=float(amount[b])
            count+=1
            
        elif str(para[b])[0:3] == "'LD":
            total+=float(amount[b])
            count+=1
            
    return[total, count]

# create tkinter window
root = tk.Tk()

# add title to window
root.title("GENERATE NIBSS REPORT")
root.geometry('1500x800')

# create button to select csv files and process them
window = tk.Frame()
window1 = tk.Frame()
frame = tk.Frame(window)
label_frame = tk.Frame(window)
text_frame = tk.Frame(window)
button_frame = tk.Frame(window)
window.pack_propagate(False)

#files_button = tk.Button(window, text="Select Files", command=get_files)
tstfiles_button = tk.Button(window, text="Get Files", command=get_all_files)
process_button = tk.Button(button_frame, text="Generate Successful Report", command=process_csv_succ_files)
save__succ_button = tk.Button(button_frame, text="Save Successful", command=save_succ_file)
save_failed_button = tk.Button(button_frame, text="Save Failed", command=save_failed_file)
process_failed_button = tk.Button(button_frame, text="Generate Failed Report", command=process_csv_unsucc_files)


label_succ = tk.Label(label_frame)
words_text = tk.Text(text_frame, height=30, width=35,state="disabled")
date_list_succ=tk.Listbox(frame,height=5,width=30)
yscrollbar_succ = tk.Scrollbar(frame, orient='vertical', command=date_list_succ.yview)
date_list_succ.config(yscrollcommand=yscrollbar_succ.set)


label_failed = tk.Label(label_frame)
words_text_failed = tk.Text(text_frame, height=30, width=35,state="disabled")
date_list_failed=tk.Listbox(frame,height=5,width=30)
yscrollbar_fail = tk.Scrollbar(frame, orient='vertical', command=date_list_failed.yview)
date_list_failed.config(yscrollcommand=yscrollbar_fail.set)
date_list_failed.pack_propagate(False)

window.pack(side="left", expand=True,fill='both')
window1.pack(side="right", expand=True,fill='both')
tstfiles_button.pack()
label_frame.pack()
frame.pack()
text_frame.pack()
button_frame.pack()

label_succ.pack(side='left')
label_failed.pack(side='left')
date_list_succ.pack(side='left')
yscrollbar_succ.pack(side='left', fill='y',expand=True)

date_list_failed.pack(side='right' )
yscrollbar_fail.pack(side='left', fill='y', expand=True)

words_text.pack(side=tk.LEFT)
words_text_failed.pack(side=tk.LEFT)

process_button.pack(side=tk.TOP,expand=True)
process_failed_button.pack(side=tk.TOP,expand=True)
save__succ_button.pack(side="bottom",expand=True)
save_failed_button.pack(side="bottom",expand=True)

get_ft_file = tk.Button(window1, text="Get Funds Transfer File", command=get_ft_transactions)
get_cs_file = tk.Button(window1, text="Get Cashout File", command=get_cash_transactions)
comms_text = tk.Text(window1, height=30, width=40,state="normal")
generate_comms = tk.Button(window1,text="GENERATE COMMISIONS",command=get_total_commision)
save_commision_file = tk.Button(window1,text="Save",command=save_file_for_commision_generator)

get_ft_file.pack()
get_cs_file.pack()
comms_text.pack()
generate_comms.pack()
save_commision_file.pack()

# run tkinter window
window.mainloop()
