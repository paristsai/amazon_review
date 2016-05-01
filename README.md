# Amazon Review Project
## 專案動機
當初在 Amazon 挑選藍牙運動耳機作為禮物時，發現想從網路商店上挑選耳機是一件很困難的事情，主要原因有 2 個：

1. 相似商品過多
2. 評價缺乏效力


#### 相似商品過多
  Amazon 商品頁由標題、價錢、敘述、規格、照片等資訊所構成，每一個因素都牽動著消費者對於該商品的看法，如果想要獲得消費者的青睞，第一印象絕對不能馬虎。但是 Amazon 上的藍芽耳機多達 8200 個，功能外型價錢相似的產品太多了，選擇太多造成的痛苦也越多。
#### 評價缺乏效力
  由於商品敘述沒有鑑別力，我把注意力轉向研究評價。但是卻發現不太對勁，有些評論旁邊寫著 Verified Purchase，有這個標籤的評論代表這個用戶是從 Amazon 購買這項商品; 旁邊沒有這個標籤代表評論者沒有從 Amazon 購買該商品，因此評論旁沒有標籤的評論者無論有沒有使用該產品的經驗，都無法被證實。事實上，有些商家使用免費耳機做為酬勞，請人在 Amazon 上寫使用心得，不用付錢就能獲得的商品當然能帶給消費者好的印象，商品評價的平均分數就會被拉高，使得其他消費者被這些過度渲染的評價影響購買決策。
  
  現代人網路購物比例越來越高，舉凡電子商品、民生用品到蔬菜水果什麼都賣什麼都不奇怪，但是也因為摸不到實品，讓人的顧慮有所增加。評價機制是網路購物不可或缺的關鍵因素，它建立起電商與消費者之間信賴的橋樑。大電商如露天、淘寶有評價造假的問題，小電商評價數量偏少，這些現象都使得我們進行網路購物時經常踩雷，Amazon 的評價機制已經算是不錯了，但是依然有進步的空間，這會在 Project2 中進一步說明。
  
  * 有標籤的評論 (請注意紅色 "Verified Purchase")
  ![alt tag](https://dl.dropboxusercontent.com/u/49401941/amazon_verified.png)
  
  * 沒有標籤的評論
  ![alt tag](https://dl.dropboxusercontent.com/u/49401941/%E8%9E%A2%E5%B9%95%E6%88%AA%E5%9C%96%202016-04-27%2023.33.18.png)


## 專案目的
根據以上發現的痛點，分別從消費者、商家、以及 Amazon 的角度思考並且設定目標：

  1. 讓消費者透過更透明的評價分析，知道哪些商品值得購買
  2. 讓商家了解 Top 100 的商品頁有什麼特色可以學習
  3. 提供 Amazon 一些建議讓這個平台變得更完備

## 專案內容
* Project 1: 進階評價查詢服務
  * 收集商品資料
    為了避免爬資料時被 Amazon 鎖 IP，一開始先在 Google App Engine 建立數個抓取網頁 html 原始碼 的代理伺服器，再從本地端透過隨機睡眠與隨機選取代理伺服器的策略以提高抓取網頁的成功率，透過 PyQuery 抓取所需的資訊後存入 SQLite 資料庫。另外如果在抓網頁時還是被擋，會把沒有成功擷取網頁的網址記錄下來，方便之後重新再抓取網頁內容。
  * 建立查詢 App
    透過 Flask 框架建立輕量 App，輸入商品編號就會到 SQLite 資料庫查詢，將查詢的結果結合 HighCharts 製作互動圖表呈現在頁面上。頁面包含有/沒有 Verified Purchase 評論的數量、比例、平均評分與評論關鍵字，並且將評論以時間序列的方式呈現，作為消費者判斷近期商品品質的依據。
  * DEMO
  ![alt tag](https://dl.dropboxusercontent.com/u/49401941/amazon_project_record2.gif)
* Project 2: 商品資料與商品評論摘要與分析              
分析過程與結果都放在 Jupyter Notebook  [請點我](http://nbviewer.jupyter.org/github/paristsai/amazon_review/blob/master/analysis/amazon-review.ipynb "Title")
  
  結合 Numpy, Pandas, Seaborn, Sklearn 等套件針對抓到的資料進行摘要與分析，試圖回答以下問題：
    * 藍牙耳機的平均價格落在哪裡？平均折扣是多少？
    * 商品敘述越詳細越能得到消費者青睞嗎？
    * 評價認證與評價分數有什麼相關性？
  

  

## 未來方向
* Project 1: 精進技術，提供更好服務
  1. 建立即時爬資料的機制
  2. 改用 PostgreSQL 做為資料庫
  3. 放到 Heroku 上讓其他人也可以使用
  4. 商品推薦模型
  5. 專案中運用到的爬蟲、代理伺服器建置與Flask建立簡單應用的教學
* Project 2: 強化分析，挖掘有用觀點
  1. 知名大廠的耳機評價和其他小廠商的評價有什麼不同？
  2. Best Seller Rank 排名較前的耳機評價越好？
  3. 哪些專業評論人最誠實？哪些評論人的評價很沒有效力？
  4. 對評論者進行分析，評論次數大於5的人是到底是網路寫手還是單純為忠誠度很高的顧客呢？

---
有什麼建議或是需要其他資訊都歡迎與我聯繫！
> **Paris Tsai**  [paristsaiswing@gmail.com](mailto:paristsaiswing@gmail.com)
