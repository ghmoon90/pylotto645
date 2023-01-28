import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests 

sz_dbfile = 'lotto_db.dat'
lotto_db = dict()

#%% db handling
def load_DB():
    global lotto_db, sz_dbfile
    with open(sz_dbfile , 'r') as file:
        lines = file.readlines()    
        #print(lines)
    #line_modi = []
    for line in lines:
        temp = line.replace('\n','').split(', ')
        keyval  = temp[0]
        lotto_db[keyval]= temp[1:8]
        print(str(lotto_db[keyval])+ '\n')
    


def db_update_excel(szfile):
    global lotto_db, sz_dbfile
    df = pd.read_excel(szfile,engine='openpyxl')
    len_df = len(df['Unnamed: 1'])
    gameid     = list(df['Unnamed: 1'][2:len_df])
    len_game = len(gameid)
    gameresult=[]
    for i in range(13,20):
        gameresult.append(list(df['Unnamed: '+str(i)][2:len_df]))        
    with open(sz_dbfile , 'w') as file:
        for k in range(0,len_game):
            #print(k)
            file.write(str(gameid[k]))
            for j in range(0,7):
                file.write(', '+str(int(gameresult[j][k]) ))
            file.write('\n')
    load_DB()
    return 1
#db_update_excel('lottodata1051.xlsx') 


def db_update_web():
    global lotto_db, sz_dbfile
    #https://dhlottery.co.kr/gameResult.do?method=allWin
    len_game = 1051
    url = 'https://dhlottery.co.kr/gameResult.do?method=allWinPrint&gubun=byWin&nowPage=&drwNoStart=1&drwNoEnd=' + str(len_game)
    with requests.get(url) as resp:
        print(resp)
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        t_body = soup.find('tbody')
    gameid = list()
    gameresult = list(np.zeros([7,len_game]))
    len_game = len(t_body.find_all('tr'))
    for i in range(0,len_game):
        gameid.append(t_body.find_all('tr')[i].find('td').text.replace('회',''))
        for j in range(0,7):
            gameresult[j][i] = (t_body.find_all('tr')[i].find_all('span')[j].text)
    with open(sz_dbfile , 'w') as file:
        for k in range(0,len_game):
            #print(k)
            file.write(str(gameid[k]))
            for j in range(0,7):
                file.write(', '+str(int(gameresult[j][k]) ))
            file.write('\n')
    load_DB()
    return 1

#%% data science 

# frequency 
def lotto_Freq():
    global lotto_db
    number = list(range(1,46))
    count = np.zeros([1,45])
    for i in range(1,len(lotto_db)+1):
        for j in range(0,6):
            temp = int(lotto_db[str(i)][j])-1
            count[0][temp] = count[0][temp] + 1 
    ascending_order = count.argsort()+1
    print('Most Frequent in all games :' +str( ascending_order[0][39:45]))
    print('Least Frequent in all games :'+ str( ascending_order[0][0:6]))
    # frequency for 100 weeks
    games100 = dict()
    for i in range(len(lotto_db) - 100 , len(lotto_db)):
        games100[str(i)] = lotto_db[str(i)]
    count = np.zeros([1,45])
    for i in range(len(lotto_db)-100,len(lotto_db)):
        for j in range(0,6):
            temp = int(games100[str(i)][j])-1
            count[0][temp] = count[0][temp] + 1 
    ascending_order = count.argsort()+1
    print('Most Frequent in last 100 games :' +str( ascending_order[0][39:45]))
    print('Least Frequent in last 100 games :'+ str( ascending_order[0][0:6]))

    # correlation 
def lotto_CoR():
    CoR = np.zeros([45,45])
    for ii in range(1, len(lotto_db)):
        temp = lotto_db[str(ii)]
        for i in range(0,7):
            ball = int(temp[i])-1
            for j in range(0,7):
                ball2 = int(temp[j])-1
                if ball != ball2 :
                    CoR[ball][ball2] = CoR[ball][ball2] +1
                    CoR[ball2][ball] = CoR[ball][ball2]
    with open('COR.txt', 'w') as f_COR:
        for i in range(0,45):        
            for j in range(0,45):
                f_COR.write(str(CoR[i][j]))
                f_COR.write('\t')
            f_COR.write('\n')
                
