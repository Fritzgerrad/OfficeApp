import pandas as pd
from helpers import dic_to_df,countify,amountify,get_freq,get_payable

class GtbParser:
    
    def __init__(self,users:str) -> None:
        df = pd.read_csv(users)
        self.data_sheet = df
        self.commision_df = None
        self.not_found_df = None
        
        
    def make_com(self,sheet:str) -> list:
        
        id_df = pd.read_csv(sheet)
        ids = id_df[id_df.columns[0]].tolist()
        
        not_found = {}
        
        users = self.data_sheet['user_id'].tolist()
        role = self.data_sheet['role'].tolist()
        agm = self.data_sheet['aggr_id'].tolist()
   
        comm = []
        agent_comm = 0
        
        for x in users:
            comm.append(0)
        
        count = get_freq(ids)
        
        for x in count:
            if x in users:
                ind = users.index(x)
                comm[ind] += count[x] * 150
                agent_comm += 1
                
                aggr = agm[ind]
                if aggr in role:
                    aggr_ind = role.index(aggr)
                    comm[aggr_ind] += count[x] * 75
                    
            else:
                not_found[x] = count[x]
                
        comm_df = self.data_sheet.copy()
        comm_df['Commission'] = comm
        comm_df['Commission After Charge'] = get_payable(comm,comm_df['bank'].tolist())
        
        total_charge = str(sum(comm) - sum(comm_df['Commission After Charge']))
        
        self.not_found_df = dic_to_df(not_found,['user_id','Count'])
        
        self.commision_df = comm_df[comm_df['Commission'] != 0] 
    
        opened_accs = str(len(id_df))
        commisioned = str(agent_comm)
        ids_provided = countify(len(count))
        ids_accounted_for = countify(len(self.commision_df))
        total_amount_paid  =  amountify(sum(self.commision_df['Commission']))
        amt_not_found = str(len(not_found))
        
        return [opened_accs,commisioned,ids_provided,ids_accounted_for,total_amount_paid,amt_not_found,total_charge]
        
    
    def get_commission(self) -> pd.DataFrame:
        return self.commision_df 
    
    
    def save_sheet(self,filename:str) -> str:
        if self.commision_df is None:
            return "Please Load and Parse the File Properly"
         
        else:
            with pd.ExcelWriter(filename) as writer:
                self.commision_df.to_excel(writer, sheet_name="Commisions",index=False)
                self.not_found_df.to_excel(writer, sheet_name="Not Found",index=False)     
                
            return "File Saved Successfully"               
                
            
            
        
        