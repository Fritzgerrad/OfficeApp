#!/usr/bin/env python3


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
from nipParser import NipParser 
from commisionParser import CommissionParser
from gtbParser import GtbParser

global commsParser
global nipParser
global gtbParser


def get_all_files():
    
    words_text.config(state="normal")
    words_text_failed.config(state="normal")
    
    
    words_text_failed.delete('1.0', tk.END)
    words_text.delete('1.0', tk.END)
    date_list_succ.delete(0,tk.END)
    date_list_failed.delete(0,tk.END)
    
    directory = filedialog.askdirectory(initialdir="/home/fritzgerrad/Documents")
    if directory == "":
        print("Please select a directory")
        return
    nipParser = NipParser(directory)
    
            
    words_text_failed.delete('1.0', tk.END)
    words_text.delete('1.0', tk.END)
    
    
    label_succ.config(text="Successful Transactions:                                    ")
    label_failed.config(text="Failed Transactions: ")
    
    
    succ_dates = nipParser.get_succ_dates()
    failed_dates = nipParser.get_failed_dates()

    for n in succ_dates:
        date_list_succ.insert(tk.END,n)
    date_list_succ.insert(tk.END,"All Available Dates")
    words_text.config(state="disabled")
    
    for n in failed_dates:
      date_list_failed.insert(tk.END,n)
    date_list_failed.insert(tk.END,"All Available Dates")
    words_text_failed.config(state="normal")
    
    words_text.config(state="normal")
    words_text.insert(tk.END,"Date Ranges for the report are: \n\n")
    words_text_failed.insert(tk.END,"Date Ranges for the report are: \n\n")
    
    succ_file_times = nipParser.succ_file_times()
    fail_file_times = nipParser.fail_file_times()

        
    for d in succ_file_times:

        amt = succ_file_times[d][0]
        count = succ_file_times[d][1]
        words_text.insert(tk.END,d+" >>\n "+count+"("+amt+")")
        words_text.insert(tk.END,"\n\n")
        
    for d in fail_file_times:

        amt = fail_file_times[d][0]
        count = fail_file_times[d][1]
        words_text_failed.insert(tk.END,d+" >>\n "+count+"("+amt+")")
        words_text_failed.insert(tk.END,"\n\n")
    
    
    words_text_failed.config(state="disabled")
    words_text.config(state="disabled")


def process_csv_succ_files():
    global DFS
    global thedate

    thedate = date_list_succ.get(tk.ACTIVE)
    
    if len(thedate) < 10:
        print ("Please Enter a Valid date")
        words_text.insert('1.0',"Please Enter a Valid date \n")
        return 0
    words_text.config(state="disabled")
    words_text.delete('1.0', tk.END)
    words_text.insert('1.0',"Generating ...")
    words_text.config(state="disabled")
    
    details = nipParser.process_succ(thedate)
    DFS = details[0]
    amts = details[1]

    words_text.config(state="normal")
    words_text.delete('1.0', tk.END)

    for x in amts:
        words_text.insert('end',x)
        words_text.insert("end","\n")

    words_text.config(state="disabled")

    for i in amts:
        print(i)
   
   
def process_csv_unsucc_files():
    global DFSS
    global thedatefailed

    words_text_failed.delete('1.0', tk.END)
    
    thedatefailed = date_list_failed.get(tk.ACTIVE)
    if len(thedatefailed) < 10:
        words_text_failed.insert('1.0',"There are no failed transactions in this report \n")
        return 0
    
    words_text_failed.config(state="disabled")
    words_text_failed.delete('1.0', tk.END)
    words_text_failed.insert('1.0',"Generating ...")
    words_text_failed.config(state="disabled")
   
    
    detailss = nipParser.process_failed(thedatefailed)
    DFSS = detailss[0]
    amtss = detailss[1]
    
    words_text_failed.config(state="normal")
    words_text_failed.delete('1.0', tk.END)
    
    for x in amtss:
        words_text_failed.insert('end',x)
        words_text_failed.insert("end","\n")

    for i in amtss:
        print(i)
  
    words_text_failed.config(state="disabled")


def save_succ_file():

    global DFS
    path_name = filedialog.asksaveasfilename(initialfile= thedate+" NIBSS SUCCSSFUL REPORT.xlsx", defaultextension=".xlsx",initialdir="/home/fritzgerrad/Documents")
    words_text.config(state="normal")
    
    words_text.insert('end',"\n \n \nWriting to File ...")
    words_text.config(state="disabled")

    status = nipParser.save_file(path_name,DFS)
        
    words_text.config(state="normal")    
    words_text.insert('end',"\n \n \nNIBBS REPORT GENERATED ")
    words_text.insert('end',"\n \n \n"+status)
    words_text.config(state="disabled")
    print("DONE")


def save_failed_file():
    global DFSS
    path_name = filedialog.asksaveasfilename(initialfile= thedate+" NIBSS FAILED REPORT.xlsx", defaultextension=".xlsx",initialdir="/home/fritzgerrad/Documents")
    words_text_failed.config(state="normal")
    
    words_text_failed.insert('end',"\n \n \nWriting to File ...")
    words_text_failed.config(state="disabled")

    status = nipParser.save_file(path_name,DFSS)
        
    words_text_failed.config(state="normal")    
    words_text_failed.insert('end',"\n \n \nNIBBS REPORT GENERATED ")
    words_text.insert('end',"\n \n \n"+status)
    words_text_failed.config(state="disabled")
    print("DONE")
    

def get_commision_files():
    global commsParser
    
    file = filedialog.askopenfile(filetypes=[("CSV Files", "*.csv")],initialdir="/home/fritzgerrad/Documents")
    if file == "" or file == None:
        print("Please select a File")
        return
    commsParser = CommissionParser(file)
    ft_count = commsParser.get_details()[0]
    cs_count = commsParser.get_details()[1]
    
    comms_text.insert(tk.END,"TOTAL FUNDS TRANSFER TRANSACTIONS: "+ft_count+"\n")
    comms_text.insert(tk.END,"TOTAL CASHOUT TRANSACTIONS: "+cs_count+"\n")


def get_total_commision():
    global commsParser
    
    comms_text.insert(tk.END,"\n")
    comms_text.insert(tk.END,"\n")
    comms_text.insert(tk.END,"\n")
    
    comm_df = commsParser.get_total_commision()
    comms_text.insert(tk.END,commsParser.display_df(comm_df))
    comms_text.config(state="disabled")
    
    
def save_file_for_commision_generator():
    comms_text.config(state="normal")
    path_name_comm = filedialog.asksaveasfilename(initialfile = "Agent Manager Commision", defaultextension=".xlsx",initialdir="/home/fritzgerrad/Documents/Commissions")
    words_text.config(state="normal")
    status = commsParser.save_file(path_name_comm)
    comms_text.insert(tk.END,"\n\n"+status)
    

def load_data_sheet():
    gtb_text.config(state='normal')

    gtb_text.delete('1.0',tk.END)
    global gtbParser
    success = ""
    file = filedialog.askopenfile()
    
    if file =="" or file is None:
        file= "/home/fritzgerrad/Documents/Full Agent Details.csv"
       
    success = "Data Sheet Loaded Successfully"
    gtbParser = GtbParser(file)
    gtb_text.insert(tk.END,success+"\n")
    gtb_text.config(state='disabled')

        
def build_gtb_sheet():
        
    gtb_text.config(state='normal')

    id_sheet = filedialog.askopenfile(initialdir="/home/fritzgerrad/Documents/GTB Documents",filetypes=[("CSV Files","*.csv")])
    
    if id_sheet is None or id_sheet=="":
        gtb_text.insert("Please select the data file \n\n")
        gtb_text.config(state='disabled')
        
    else:
        dets = gtbParser.make_com(id_sheet)
        gtb_text.insert(tk.END,"The Number of Presented IDs are: "+dets[0]+"\n\n")
        gtb_text.insert(tk.END,"The Number of Billed IDs "+dets[1]+"\n\n")
        gtb_text.insert(tk.END,"Customers who Opened Accounts "+dets[2]+"\n\n")
        gtb_text.insert(tk.END,"Customers who Opened Accounts Found "+dets[3]+"\n\n")
        gtb_text.insert(tk.END,"Customers who Opened Accounts Not Found "+dets[5]+"\n\n")
        gtb_text.insert(tk.END,"The total amount calculated to be paid out "+dets[4]+"\n\n")
        gtb_text.insert(tk.END, "The total Charge to be paid is "+dets[6]+"\n\n")
        gtb_text.config(state='disabled')

             
def save_gtb_sheet():
    gtb_text.config(state='normal')

    sheetname = filedialog.asksaveasfilename(initialfile="GTB Account Opening Commission",defaultextension=".xlsx")
    save_message = gtbParser.save_sheet(sheetname)
    gtb_text.insert(tk.END,save_message)
    gtb_text.config(state='disabled')   

 
# create tkinter window
root = tk.Tk()

# add title to window
root.title("GENERATE NIBSS REPORT")
root.geometry('1800x800')

window = tk.Frame()
window1 = tk.Frame()
#window3 = tk.Frame()

gtb_frame = tk.Frame()
frame = tk.Frame(window)
label_frame = tk.Frame(window)
text_frame = tk.Frame(window)
button_frame = tk.Frame(window)
window.pack_propagate(False)

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

window.pack(side="left", expand=True,fill='both',ipadx='100')
window1.pack(side="right",ipadx='100')
gtb_frame.pack(side='right',ipadx='100')


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


get_trx_file = tk.Button(window1, text="Get Transaction File", command=get_commision_files)
comms_text = tk.Text(window1, height=40, width=60,state="normal")
generate_comms = tk.Button(window1,text="GENERATE COMMISIONS",command=get_total_commision)
save_commision_file = tk.Button(window1,text="Save",command=save_file_for_commision_generator)


load_data_button  = tk.Button(gtb_frame, text="Load Data Sheet",command=load_data_sheet)
gtb_text = tk.Text(gtb_frame,height=40, width=60,state='disable')
make_gtb_comms = tk.Button(gtb_frame,text="Calculate Commissions",command=build_gtb_sheet)
save_gtb_comms = tk.Button(gtb_frame,text="Save GTB Comm",command=save_gtb_sheet)


load_data_button.pack()
gtb_text.pack()
make_gtb_comms.pack()
save_gtb_comms.pack()


gtb_frame.pack()
get_trx_file.pack()
comms_text.pack()
generate_comms.pack()
save_commision_file.pack()


# run tkinter window
window.mainloop()
