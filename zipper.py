import zipfile
import pandas as pd
import os

class Zipper():
    
    def __init__(self,directory:str) -> None:
        self.directory = directory
        self.succ_files = self.make_df_from_directory("NIP_894_outwards successful.csv")
        self.fail_files = self.make_df_from_directory("NIP_894_outwards unsuccessful.csv")


    def get_zip(self,zip_file:zipfile, contains_string:str) -> list:
     
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
                        ' PAYMENT REFERENCE', 'LAST 12 DIGITS OF SESSION_ID'],encoding_errors='ignore')
                            #display_count(input_df,thedate,i)  
                        dataframe_list.append(df)
                        os.remove(file_path)
                    elif name.endswith('.csv') or name.endswith('.txt') or name.endswith('.pdf'):
                        os.remove(file_path) # delete the processed zip file        
        #return dataframe_list[0][['AMOUNT', ' PAYMENT REFERENCE','TRANSACTION TIME']]
        return dataframe_list


    def make_df_from_directory(self,contains_string:str)-> dict:
        file_times = {}  
        
        
        #dataframe_list = []
        for root, dirs, files in os.walk(self.directory, topdown=False):
            for name in files:
                if name.endswith('.csv') and contains_string in name:
                    file_path = os.path.join(root, name)
                    df = pd.read_csv(file_path)
                    #dataframe_list.append(df)
                    if not "unsuccessful" in contains_string:
                        file_times[name] = df
                    else:
                        file_times[name] = df
                elif name.endswith('.zip'):
                    file_path = os.path.join(root, name)                 
                    zip_dataframes_list = self.get_zip(file_path, contains_string)
                    if len(zip_dataframes_list) == 1:
                        zip_dataframes = zip_dataframes_list[0]
                        #dataframe_list += zip_dataframes
                        if not "unsuccessful" in contains_string:
                            file_times[name[52:63]] = zip_dataframes
                        else:
                            file_times[name[52:63]] = zip_dataframes
                        
        #return pd.concat(list(files.values()))
        return file_times


    def get_successful(self) -> dict:
        return self.succ_files
   
   
    def get_failed(self)-> dict:
       return self.fail_files

    
