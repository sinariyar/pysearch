# 導入 模組 
import requests 

key=input('請輸入關鍵字: ')
page = int(input("請輸入需要收尋的頁數: "))  #最新的頁數往回推
URL = "https://www.ptt.cc/bbs/Gossiping/index.html"
    
# 設定Header與Cookie
my_headers = {'cookie': 'over18=1;'}

# 發送get 請求 到 ptt 時是版
response = requests.get(URL, headers = my_headers)

# 導入 BeautifulSoup 模組：解析HTML 語法工具
import bs4
        
# 把網頁程式碼(HTML) 丟入 bs4模組分析
soup = bs4.BeautifulSoup(response.text,"html.parser")
# print(soup)

u = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
# [<a class="btn wide" href="/bbs/Gossiping/index1.html">最舊</a>, 
# <a class="btn wide" href="/bbs/Gossiping/index39300.html">‹ 上頁</a>, 
# <a class="btn wide disabled">下頁 ›</a>, 
# <a class="btn wide" href="/bbs/Gossiping/index.html">最新</a>]

url_str = u[1]["href"]  #上一頁按鈕的網址
# /bbs/Gossiping/index39292.html

s = url_str.strip("/bbs/Gossiping/index.html") #刪除特定字元
# '39292'
n = int(s)  #字串轉換成整數
n += 1      #最新的頁數
# '39293'
# In[]
# 把 ptt 時是版網址存到 URL 變數中
# 把之前學的for迴圈拿出來用
for j in range(n-page,n+1):
    URL = "https://www.ptt.cc/bbs/Gossiping/index"+str(j)+".html"
    
    # 設定Header與Cookie
    my_headers = {'cookie': 'over18=1;'}
    
    # 發送get 請求 到 ptt 時是版
    response = requests.get(URL, headers = my_headers)
    
    # 把網頁程式碼(HTML) 丟入 bs4模組分析
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    
    #抓取我們想要的目標
    titles = soup.find_all('div','title')

    # 萃取文字出來
    # for t in titles:
    #     print(t.text)
        
    # 存取成csv檔

    #導入 pandas 模組
    import pandas as pd
    
    # 創建一個空的list
    title_list = []
    
    # 將萃取出來的文字存入我們創建的list中
    for t in titles:
        title_list.append(t.text)
    
    
    # 將list 改成能存取成csv的格式
    df = pd.DataFrame()
    
    # 給予列標題
    df ['title'] = title_list
    
    # 改變存檔名稱
    df.to_csv("./data/"+str(j)+'.csv',index=False,encoding="utf-8-sig")
    
# In[]
#讀取文件資料夾之位置的模組
from glob import glob 

# 讀取資料夾下的檔案
files = glob(r'C:\Users\q1217\Desktop\Topic\T8\data\*.csv')

# 合併檔案
df = pd.concat(
    (pd.read_csv(file, usecols=['title'], encoding='utf-8-sig') for file in files), ignore_index=True)

# 存取檔案
df.to_csv('./data/data.csv',index=False,encoding='utf-8-sig')


#讀取csv檔
df = pd.read_csv('./data/data.csv')
# print(df)

#尋找關鍵字
mvc = df.loc[df['title'].str.contains(key)]
print(mvc)

#存取檔案
mvc.to_csv('./data/keyword.csv', index=False,encoding='utf-8-sig')

# In[]