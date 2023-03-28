import pandas as pd

class Table():
    def __init__(self, rows, columns):
        self.columns = []
        self.num_columns = columns
        self.num_rows = rows
        
        for x in columns:
            column = []
            for y in rows:
                column.append(None)
            self.columns.append(column)
            
    def __str__(self):
        for a in self.columns:
            return a
                

    def check_authenticity(self):
        auth = len(self.columns[0])
        for i in self.columns:
            if len (i) != auth:
                return False
        
        return True
    
    def fill(self):
        auth = self.columns[0]
        for i in self.columns:
            if len(i) > auth:
                j = len(i) - auth
                while j < len(i)+1:
                    for x in self.columns:
                        x.append(None)
                    j+=1
                    
            if len(i) < auth:
                j = auth - len(i)
                while j < auth :
                    for x in self.columns:
                        x.append(None)
                    j+=1
        
    def table_from_df(self, df):
        headers = df.columns
        for a in headers:
            self.columns.append(df[a].tolist())
            
        if self.check_authencity():
            self.num_columns =  len(self.columns)
            self.num_rows = len(self.columns[0])

            return self
    
    
    def get_similar(self,outlist,col):
        ans=[]
        for ab in self.columns:
            tmp = []
            ans.append(tmp)
                     
        for a in range(len(self[col])):
            if self.columns[a]  in outlist:
                for v in range(len(self)):
                    ans[v].append(self[v][a])   
                             
        return ans 
    
    
    def get_difference(self,outlist,col):
        ans=[]
        for ab in self.columns:
            tmp = []
            ans.append(tmp)
                     
        for a in range(len(self[col])):
            if self.columns[a] not in outlist:
                for v in range(len(self)):
                    ans[v].append(self[v][a])   
                    
        return ans
    
    
    def table_to_df(self,headers):
        if len(self.columns) != len(headers):
            return "Header is not appropriate"
        
        thedict = {}
        for x in range(len(self)):
            thedict[headers[x]]=self[x]
            
        df =pd.DataFrame(thedict)    
        return df
    
    
    def replace_element(self,row,column,element):
        self[column][row] = element
        
    
    def insert_column(self,column):
        self.columns.append(column)
        self.fill()
        self.num_columns = self.num_columns+1
        
        
    def insert_column_at(self,column,index):
        if index == "end":
            index = len(self.columns)-1 
                            
        pos = index   
        c = len(self) - 1       
        while c < pos:
            self.append(None)
            self[c] = self[c+1]
            c-=1
        self[pos] = (column) 
        self.num_columns += 1
        self.num_rows +=1
        
        
    def find(self, element):
        for x in range(len(self)):
            for y in range(len(y)):
                if element in self[x]:
                    
                    return x,y
        
    def find_all(self,element):
        ans = []
        for x in range(len(self)):
            for y in range(len(y)):
                if element in self[x]:
                    curr = [x,y]
                    ans.append(curr)
                    
        return ans
    
    
    def frequency(self,element):
        return(len(self.find_all(element)))
          
    def insert_row(self):
        pass
    
    def insert_element_at(self,row,column,element):
        if len(self) < column:
            pass
        
        if len