import pandas as pd
from zipper import Zipper
from helpers import *

class NipParser:    
    
    def __init__(self,directory:str) -> None:

        
        print("Loading Dataframes")
        zee = Zipper(directory)
        self.files_succ = dict(sorted(zee.get_successful().items()))
        
        self.files_fail = dict(sorted(zee.get_failed().items()))
        
        datafs = list(self.files_fail.values())
        self.df_succ = pd.concat(list(self.files_succ.values()))
        self.df_fail = pd.concat(datafs)
        
        
        print("DataFrames successfully Loaded")
        
        
    def get_succ_dates(self) -> list:
        return get_dates(self.df_succ)
    
    
    def get_failed_dates(self) -> list:
        return get_dates(self.df_fail)
        
        
    def succ_file_times(self) -> dict:
        x = {}
        for d in self.files_succ:
            x[datify(d)] = get_range_amount(self.files_succ[d])
            
        return x
    
    
    def fail_file_times(self) -> dict:
        x = {}
        for d in self.files_fail:
            x[datify(d)] = get_range_amount(self.files_fail[d])
            
        return x
            
            
    def process_succ(self,the_date:str) -> tuple:
       
        headers = self.df_succ.columns
        SUCC = populate_lists(self.df_succ,the_date)
        
        DFS = []
        
        for x in range(4):
            DFS.append(save_df(SUCC[x], headers))
            
        amts = []
            
        for x in range(len(DFS)):
            curr = [float(a) for a in DFS[x]['AMOUNT'].tolist()]
            amts.append(curr)
            
        mlen ="MC: "+countify(len(DFS[0]))+" ("+amountify(sum(amts[0]))+")"
        clen = "CH: "+countify(len(DFS[1]))+" ("+amountify(sum(amts[1]))+")"
        vlen = "VD: "+countify(len(DFS[2]))+" ("+amountify(sum(amts[2]))+")"
        llen ="LD: "+countify(len(DFS[3]))+" ("+amountify(sum(amts[3]))+")"

        amounts = [mlen,clen,vlen,llen]

        return DFS,amounts
    
    
    def process_failed(self,the_date:str) -> tuple:
       
        headers = self.df_fail.columns
        FAILED = populate_lists(self.df_fail,the_date)
        
        DFSS = []
        
        for x in range(4):
            DFSS.append(save_df(FAILED[x], headers))
            
        amtss = []
            
        for x in range(len(DFSS)):
            curr = [float(a) for a in DFSS[x]['AMOUNT'].tolist()]
            amounts.append(curr)
            
        mlen ="MC: "+str(len(DFSS[0]))+" ("+amountify(sum(amtss[0]))+")"
        clen = "CH: "+str(len(DFSS[1]))+" ("+amountify(sum(amtss[1]))+")"
        vlen = "VD: "+str(len(DFSS[2]))+" ("+amountify(sum(amtss[2]))+")"
        llen ="LD: "+str(len(DFSS[3]))+" ("+amountify(sum(amtss[3]))+")"

        amounts = [mlen,clen,vlen,llen]
        
        return DFSS,amounts


    def save_file(self,path_name,df_list) -> str:
        try: 
        
            with pd.ExcelWriter(path_name) as writer:
            
                df_list[0].to_excel(writer, sheet_name="MC",index=False)
                df_list[1].to_excel(writer, sheet_name="CH",index=False)
                df_list[2].to_excel(writer, sheet_name="VD",index=False)
                df_list[3].to_excel(writer, sheet_name="LD",index=False)
                
            return "File Save Successfully"
        
        except:
            
            return "An Error Occurred"
            

                
            
        

        
