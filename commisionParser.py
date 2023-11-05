import pandas as pd
pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None) 

from helpers import *

class CommissionParser:
    
    def __init__(self,file:str) -> None:
        try:
            df  = pd.read_csv(file,encoding='unicode_escape')
            self.df_FT = df[df['transaction_type_id'] == 4]
            self.df_CS = df[df['transaction_type_id'] == 3]
            self.ft_commission = None
            self.cs_commission = None
            self.total_commision = None
        except:
            print("Please select a valid File")
        
        
    def get_details(self) -> tuple:
        return countify(len(self.df_FT)),countify(len(self.df_CS))
    
    
    def get_conv_fees(self)-> pd.DataFrame:
        conv_df = pd.DataFrame()
        types = ['Funds Transfer','Cash out']
        count = [countify(len(self.df_FT)),countify(len(self.df_CS))]
        amt = [amountify(sum(self.df_FT['conv'])),amountify(sum(self.df_CS['conv']))]
        conv_df['type'] = types
        conv_df['Count'] = count
        conv_df['Amount'] = amt
        
        return conv_df

    
    def get_int_fee(self) -> pd.DataFrame:
        int_fee_df = pd.DataFrame()
        int_fee = sum([min(x*0.003,20) for x in self.df_CS['CS Amount']])
        int_fee_df['type'] = ['Interswitch Fee']
        int_fee_df['Count'] = countify(len(self.df_CS))
        int_fee_df['Amount'] =  amountify(int_fee)
        
        return int_fee_df
    
    
    def make_ft_commision(self) -> dict:
        ans={}
        agms = self.df_FT['Agent Managers'].tolist()

        for x,y in enumerate(agms):
            ans[y] = ans.get(y,0) + 1
        
        return ans
    
    
    def make_cs_commision(self) -> dict:
        ans={}
        cs_comms = get_cs_commision(self.df_CS['CS Amount'].tolist())
        agms = self.df_CS['Agent Managers'].tolist()

        
        for x,y in enumerate(agms):
            if y in ans:
                ans[y] += cs_comms[x]
                
            else:
                ans[y] = cs_comms[x]
        
        
        for c in ans:
            ans[c] = int(ans[c] + 0.5)
        return ans
        
    
    def make_commisions(self) -> bool:       

        total_comms = {}
        total_comms_df = pd.DataFrame()
        
        ft_comm = self.make_ft_commision()
        cs_comm = self.make_cs_commision()
        
        self.cs_commission = dic_to_df(cs_comm,['Agent Managers','Commissions'])
        self.ft_commission = dic_to_df(ft_comm,['Agent Managers','Commissions'])
        
        for i in ft_comm.keys():
            if i in total_comms:
                total_comms[i] = total_comms[i] + ft_comm[i]
                
            else:
                total_comms[i] = ft_comm[i]
                
        for i in cs_comm.keys():
            if i in total_comms:
                total_comms[i] = total_comms[i] + cs_comm[i]
                
            else:
                total_comms[i] = cs_comm[i]
                
        total_comms = dict(sorted(total_comms.items(),key=lambda x:x[1],reverse=True))
        
        agms,amt = [],[]
        
        for key, value in total_comms.items():
            agms.append(key)
            amt.append(value)
        
        total_comms_df["Agent Managers"] =  agms
        total_comms_df["Commissions"] = amt
        
        self.total_commision = total_comms_df
        
        if self.total_commision is None or self.ft_commission is None or self.cs_commission is None:
            return False
        
        else:
            return True
        
        
    def get_total_commision(self)-> pd.DataFrame:
        if self.total_commision is None:
            self.make_commisions()
            
        return self.total_commision
    
    
    def get_ft_commission(self)-> pd.DataFrame:
        if self.ft_commission is None:
            self.make_commisions()
            
        return self.ft_commission
    
    
    def get_cs_commission(self)-> pd.DataFrame:
        if self.cs_commission is None:
            self.make_commisions()
            
        return self.cs_commission
    
    
    def get_others(self)-> pd.DataFrame:
        empty = pd.DataFrame()
        empty['type'] = [' ',' ']
        empty['Count'] = [' ',' ']
        empty['Amount'] = [' ',' ']
        return pd.concat([self.get_conv_fees(),empty,self.get_int_fee()])


    def save_file(self,path_name_comm:str)-> str:
        df_funds = self.get_ft_commission()
        df_cash = self.get_cs_commission()
        df_total = self.get_total_commision()
        others = self.get_others()
        
        try:

            with pd.ExcelWriter(path_name_comm) as writer:
                df_funds.to_excel(writer, sheet_name="Fund Transfer Commisions",index=False)
                df_cash.to_excel(writer, sheet_name="Cash Out Commisions",index=False)
                df_total.to_excel(writer, sheet_name="Total Commisions",index=False)
                others.to_excel(writer, sheet_name="Others",index=False)
                
            return "File Save Successfully"
        
        except:
            return "An Error Occurred"
  
            
    def display_df(self,df:pd.DataFrame) -> str:
        super_lists = []
        super_str = ""
        
        for x in df.columns:
            super_lists.append(df[x].tolist()) 
            
        maxlength = 0
            
        for x in super_lists[0]:
            if len(x) > maxlength:
                maxlength = len(x)

            
        for x in range(len(super_lists[0])):
            for w,y in enumerate(super_lists):
                curr = y[x]
                if w == 0:
                    z = maxlength - len(curr)
                    for a in range(z):
                        curr+=" "
                    super_str+= curr
                elif w == 1:
                    num = int(curr +0.5) 
                    super_str+= countify(num)
                super_str+="    "
            super_str+="\n"
            
        return super_str       
        
        
        
        
