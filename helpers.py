import pandas as pd

def get_lists(df:pd.DataFrame) -> list:
    ans = []
    for a in df.columns:
        ans.append(df[a].tolist())
    return ans
       
        
def get_column(df:pd.DataFrame, col_name:str) -> list:
    for a in df.columns:
        if col_name.upper() in a.upper():
            return df[a].tolist()
   
        
def put(patner:list,dflist:list,dex:int) -> None:
    for i in range(len(dflist)):
        patner[i].append(dflist[i][dex])
        

def populate_lists(df:pd.DataFrame,day:str) -> list:
    para = get_column(df,"PAYMENT")
    date = get_column(df,"TIME")
    lists = get_lists(df)
    list_len = len(lists)
    
    out = []
    for i in range(4):
        curr = []
        for x in range(list_len):
            temp = []
            curr.append(temp)
            
        out.append(curr)
            
        
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
                     
                     
    return out

          
def save_df(pat:list,headers:list) -> pd.DataFrame:
    df = pd.DataFrame()
    for h in range(len(headers)):
       header = headers[h]
       df[header]=pat[h]
    return df


def get_dates(df:pd.DataFrame) -> list:
    unique_dates =[]
    all_d = get_column(df,"TIME")
    all_d = [str(t)[1:11] for t in all_d]
    for g in all_d:
        if g not in unique_dates and "20" in g:
            unique_dates.append(g)
    return sorted(unique_dates)


def amountify(amount:float) -> str:
    total_num = str(amount).split(".")
    integer = int(total_num[0])
    format_string = str("N {:,.0f}".format(integer))
    try: 
        return format_string +"."+total_num[1][:4]
    except:
        return str(amount)


def countify(num:int) -> str:
    formatted_amount = "{:,.0f}".format(num)
    return formatted_amount


def get_range_amount(df:pd.DataFrame) -> list:
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
            
    return[amountify(total), countify(count)]
      

def get_cs_commision(the_list:list)-> list:
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


def dic_to_df(dic:dict,headers:list) -> pd.DataFrame:
    new_df = pd.DataFrame()
    new_df[headers[0]] = list(dic.keys())
    new_df[headers[1]] = list(dic.values())
    
    return new_df
    
    
def datify(thedate:str) ->str:
    months = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'
    }
    return thedate[2:4] + " " + months[thedate[0:2]] +" "+thedate[5:7]+ ":" +thedate[7:9] + ":" +thedate[9:]
    
    
def get_freq(names:list) -> dict:
    freq = {}
    
    for i in names:
        freq[i] = freq.get(i,0) + 1
        
    return freq


def get_payable (amts:list, banks:list) -> list:
        payable = []
        for x,y in enumerate(amts):
            
            charge = (y * 0.001)
            if banks[x] != 'GTB':
                if y < 50001:
                    charge += 10
                elif y > 5000 and y < 10001:
                    charge += 25
                    
                elif y > 10000 and y < 50001:
                    charge += 75

                elif y > 50000:
                    charge += 100  
            else:
                charge+= 15
                
            payable.append(y - charge)
            
        return payable     