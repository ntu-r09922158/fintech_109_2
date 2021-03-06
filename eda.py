# -*- coding: utf-8 -*-
"""EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ps_AF0JxznzwMd1CylL_IsaQ7pv0MfFp
"""

import os, time, glob, socket, pickle
import matplotlib.pyplot as plt
import matplotlib.pyplot as mp, seaborn
import numpy as np
import numpy.linalg as LA
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
import seaborn as sns 
import math

from google.colab import drive
drive.mount('/content/gdrive') # 此處需要登入google帳號
# 獲取授權碼之後輸入即可連動雲端硬碟
train_file = pd.read_csv("/content/gdrive/My Drive/Colab/FinTech/data/train_new.csv")

# 新的資料集：總共有1141340筆資料，22個變數，跟一個Y
train_file.shape

train_file.head()

"""**資料說明**   
*  總比數：1141340
*  授權期間：1-120日  
*  訓練集：1-90日  
*  測試集：91-120日
---
**欄位說明(數字代表類別總數)**

*   acqic：收單行代碼  [categorical] 5524
*   bacno：歸戶帳號  [categorical] 92602
*   cano：交易卡號  [categorical] 124310
*   conam：交易金額-台幣 [numeric] 
*   contup：交易類型  [categorical] 7
*   csmcu：消費地幣別  [categorical] 66
*   ecfg：網路交易註記  [dummy] 2
*   etymd：交易型態  [categorical] 11
*   flbmk：Fallback 註記  [dummy] 2
*   flg_3dsmk：3DS 交易註記  [dummy] 2
*   hcefg：支付形態  [categorical] 9
*   insfg：分期交易註記  [dummy] 2
*   iterm：分期期數  [categorical] 9
*   locdt：授權日期  [numeric] 
*   loctm：授權時間  [numeric] 
*   mcc：MCC_CODE  [categorical] 418
*   mchno：特店代號  [categorical] 78435
*   ovrlt：超額註記碼  [dummy] 2
*   scity：消費城市  [categorical] 5026
*   stocn：消費地國別  [categorical] 98
*   stscd：狀態碼  [categorical] 5
*   txkey：交易序號  [categorical] - 從模型中移除，為是ID

*   fraud_ind：盜刷註記  [dummy] 2
"""

train_file.columns

# 其中，有遺失值的變數為flbmk與flg_3dsmk
train_file.isnull().sum()

# 1141340，代表 flbmk 發生缺漏值的觀察值與 flg_3dsmk 發生缺漏值的觀察值都一樣
sum(train_file['flbmk'].isnull() == train_file['flg_3dsmk'].isnull())

"""### Exploratory Data Analysis

#### For Y：fraud_ind
"""

# 總共只有 1.3%的資料為盜刷
sum(train_file['fraud_ind'])/len(train_file['fraud_ind'])

print(train_file['fraud_ind'].value_counts(sort = False))
sns.set()
plt.title("Histogram of fraud_ind",fontsize=15)
sns.countplot(train_file['fraud_ind'])

"""#### For X：'acqic', 'bacno', 'cano', 'conam', 'contp', 'csmcu', 'ecfg', 'etymd', 'flbmk', 'flg_3dsmk', 'hcefg', 'insfg', 'iterm', 'locdt', 'loctm', 'mcc', 'mchno', 'ovrlt', 'scity', 'stocn', 'stscd', 'txkey'

#### 是數字但是為類別型態的資料：acqic, bacno, cano, contp, csmcu, etymd, hcefg, iterm, mcc, mchno, scity, stocn, stscd

##### acqic：收單行代碼
"""

print(len(np.unique(train_file['acqic'])))
print(np.unique(train_file['acqic']))
print(train_file['acqic'].value_counts())
# sns.set()
# sns.countplot(train_file['acqic'])

"""#####  bacno：歸戶帳號"""

print(len(np.unique(train_file['bacno'])))
print(np.unique(train_file['bacno']))
print(train_file['bacno'].value_counts())
# sns.set()
# sns.countplot(train_file['bacno'])

df0 = train_file[train_file['fraud_ind'] == 0]
df1 = train_file[train_file['fraud_ind'] == 1]

df_bacno = pd.DataFrame(np.array(df1['bacno'].value_counts()), index = df1['bacno'].value_counts().index, columns=['bacno']).iloc[0:10]
plt.figure(figsize = (18,6))
x = ['36103', '156870', '159452',' 118402', '77441', '46582', '91688', '140259', '107667','97832']
y = df_bacno['bacno']

plt.bar(x,y)
plt.xlabel('BACNO')
plt.ylabel('Cumulative Count')
plt.title('Top 10 BACNO with cumulative count of Fraud Transaction', fontsize = 18)
plt.show()

"""##### cano：卡號"""

print(len(np.unique(train_file['cano'])))
print(np.unique(train_file['cano']))
print(train_file['cano'].value_counts())
# sns.set()
# sns.countplot(train_file['cano'])

df1[df1['bacno'] == 36103]['cano']

df_cano = pd.DataFrame(np.array(df1['cano'].value_counts()), index = df1['cano'].value_counts().index, columns=['cano']).iloc[0:10]
plt.figure(figsize = (18,6))
x = ['100698', '24682', '155642', '182908', '206437', '55762', '206464', '42331', '17315', '161690']
y = df_cano['cano']

plt.bar(x,y)
plt.xlabel('CANO')
plt.ylabel('Cumulative Count')
plt.title('Top 10 CANO with cumulative count of Fraud Transaction', fontsize = 18)
plt.show()

"""##### contp：交易類別"""

print(len(np.unique(train_file['contp'])))
print(np.unique(train_file['contp']))
print(train_file['contp'].value_counts(sort = False))
sns.set()
sns.countplot(train_file['contp'])

"""##### csmcu：消費地幣別"""

print(len(np.unique(train_file['csmcu'])))
print(np.unique(train_file['csmcu']))
print(train_file['csmcu'].value_counts(sort = False))
sns.set()
sns.countplot(train_file['csmcu'])

"""##### etymd：交易型態"""

print(len(np.unique(train_file['etymd'])))
print(np.unique(train_file['etymd']))
train_file['etymd'].value_counts(sort = False)
sns.set()
sns.countplot(train_file['etymd'])

"""##### hcefg：支付形態"""

print(len(np.unique(train_file['hcefg'])))
print(np.unique(train_file['hcefg']))
print(train_file['hcefg'].value_counts(sort = False))
sns.set()
sns.countplot(train_file['hcefg'])

"""##### iterm：分期期數"""

print(len(np.unique(train_file['iterm'])))
print(np.unique(train_file['iterm']))
print(train_file['iterm'].value_counts())
plt.hist(train_file['iterm'])
plt.show()

"""##### mcc：特店類型"""

print(len(np.unique(train_file['mcc'])))
print(np.unique(train_file['mcc']))
print(train_file['mcc'].value_counts(sort = False))
# sns.set()
# sns.countplot(train_file['mcc'])

"""##### mchno：特店名稱"""

print(len(np.unique(train_file['mchno'])))
print(np.unique(train_file['mchno']))
print(train_file['mchno'].value_counts())
# sns.set()
# sns.countplot(train_file['mchno'])

"""#####  scity：消費城市"""

print(len(np.unique(train_file['scity'])))
print(np.unique(train_file['scity']))
print(train_file['scity'].value_counts())
# sns.set()
# sns.countplot(train_file['scity'])

"""##### stocn：消費地國別"""

print(len(np.unique(train_file['stocn'])))
print(np.unique(train_file['stocn']))
print(train_file['stocn'].value_counts())
sns.set()
sns.countplot(train_file['stocn'])

"""##### stscd：狀態碼"""

print(len(np.unique(train_file['stscd'])))
print(np.unique(train_file['stscd']))
print(train_file['stscd'].value_counts(sort = False))
sns.set()
sns.countplot(train_file['stscd'])

print(len(np.unique(train_file['txkey'])))

"""##### Y/N變數：ecfg, flbmk, flg_3dsmk, insfg, ovrlt

##### ecfg：網路交易註記
"""

print(len(np.unique(train_file['ecfg'])))
print(np.unique(train_file['ecfg']))
print(train_file['ecfg'].value_counts(sort = False))
sns.set()
sns.countplot(train_file['ecfg'])

"""##### flbmk：fallback註記"""

# 因為'flbmk'有遺失值，為了看出結果先刪除再看分布(但不會刪原始資料的)
flbmk = train_file['flbmk']
flbmk = flbmk.dropna()
flbmk

print(len(np.unique(flbmk)))
print(np.unique(flbmk))
print(flbmk.value_counts())
sns.set()
sns.countplot(train_file['flbmk'])

"""##### flg_3dsmk：3DS交易驗證註記"""

# 因為'flg_3dsmk'有遺失值，為了看出結果先刪除再看分布(但不會刪原始資料的)
flg_3dsmk = train_file['flg_3dsmk']
flg_3dsmk = flg_3dsmk.dropna()
print(len(np.unique(flg_3dsmk)))
print(np.unique(flg_3dsmk))
print(flg_3dsmk.value_counts())
sns.set()
sns.countplot(train_file['flg_3dsmk'])

"""##### insfg：分期交易註記"""

print(len(np.unique(train_file['insfg'])))
print(np.unique(train_file['insfg']))
print(train_file['insfg'].value_counts())
sns.set()
sns.countplot(train_file['insfg'])

"""##### ovrlt：超額註記碼"""

print(len(np.unique(train_file['ovrlt'])))
print(np.unique(train_file['ovrlt']))
print(train_file['ovrlt'].value_counts())
sns.set()
sns.countplot(train_file['ovrlt'])

"""以下做的是：以各變數的值作為分母，各變數的值且是否為盜刷作為分子"""

# Y = 0 與 Y = 1 的比例
print(round(train_file[train_file['fraud_ind'] == 0].shape[0]/train_file.shape[0], 3))
print(round(train_file[train_file['fraud_ind'] == 1].shape[0]/train_file.shape[0], 3))

# ecfg = N & ecfg = Y 其中 Y = 0 與 Y = 1 的比例
print(round(train_file[(train_file['ecfg'] == 'N') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['ecfg'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['ecfg'] == 'N') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['ecfg'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['ecfg'] == 'Y') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['ecfg'] == 'Y'].shape[0], 3))
print(round(train_file[(train_file['ecfg'] == 'Y') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['ecfg'] == 'Y'].shape[0], 3))

# flbmk = N & flbmk = Y 其中 Y = 0 與 Y = 1 的比例：非遺失值的(drop missing)
print(round(train_file[(train_file['flbmk'] == 'N') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['flbmk'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['flbmk'] == 'N') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['flbmk'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['flbmk'] == 'Y') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['flbmk'] == 'Y'].shape[0], 3))
print(round(train_file[(train_file['flbmk'] == 'Y') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['flbmk'] == 'Y'].shape[0], 3))

# flbmk missing 中的 Y = 0 與 Y = 1 的比例
print(1-round(train_file[train_file['flbmk'].isnull() == True]['fraud_ind'].sum()/train_file[train_file['flbmk'].isnull() == True].shape[0], 3))
print(round(train_file[train_file['flbmk'].isnull() == True]['fraud_ind'].sum()/train_file[train_file['flbmk'].isnull() == True].shape[0], 3))

# flg_3dsmk = N & flg_3dsmk = Y 其中 Y = 0 與 Y = 1 的比例：非遺失值的(drop missing)
print(round(train_file[(train_file['flg_3dsmk'] == 'N') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['flg_3dsmk'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['flg_3dsmk'] == 'N') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['flg_3dsmk'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['flg_3dsmk'] == 'Y') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['flg_3dsmk'] == 'Y'].shape[0], 3))
print(round(train_file[(train_file['flg_3dsmk'] == 'Y') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['flg_3dsmk'] == 'Y'].shape[0], 3))

# flg_3dsmk missing 中的 Y = 0 與 Y = 1 的比例
print(1-round(train_file[train_file['flg_3dsmk'].isnull() == True]['fraud_ind'].sum()/train_file[train_file['flg_3dsmk'].isnull() == True].shape[0], 3))
print(round(train_file[train_file['flg_3dsmk'].isnull() == True]['fraud_ind'].sum()/train_file[train_file['flg_3dsmk'].isnull() == True].shape[0], 3))

# insfg = N & insfg = Y 其中 Y = 0 與 Y = 1 的比例
print(round(train_file[(train_file['insfg'] == 'N') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['insfg'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['insfg'] == 'N') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['insfg'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['insfg'] == 'Y') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['insfg'] == 'Y'].shape[0], 3))
print(round(train_file[(train_file['insfg'] == 'Y') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['insfg'] == 'Y'].shape[0], 3))

# ovrlt = N & ovrlt = Y 其中 Y = 0 與 Y = 1 的比例
print(round(train_file[(train_file['ovrlt'] == 'N') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['ovrlt'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['ovrlt'] == 'N') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['ovrlt'] == 'N'].shape[0], 3))
print(round(train_file[(train_file['ovrlt'] == 'Y') & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['ovrlt'] == 'Y'].shape[0], 3))
print(round(train_file[(train_file['ovrlt'] == 'Y') & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['ovrlt'] == 'Y'].shape[0], 3))

"""以下做的是：以 fraud_ind = 0 或 fraud_ind = 1 為分母，該變數為 N 或 Y 且 fraud_ind = 0 或 fraud_ind = 1 為分子：ecfg, flbmk, flg_3dsmk, insfg, ovrlt"""

# 在 fraud_ind = 0 的情況下，ecfg = N & ecfg = Y 的比例
print(round(train_file[(train_file['ecfg'] == "N") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
print(round(train_file[(train_file['ecfg'] == "Y") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
# 在 fraud_ind = 1 的情況下，ecfg = N & ecfg = Y 的比例
print(round(train_file[(train_file['ecfg'] == "N") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))
print(round(train_file[(train_file['ecfg'] == "Y") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))

# 在 fraud_ind = 0 的情況下，flbmk = N & flbmk = Y & flbmk = nan 的比例
print(round(train_file[(train_file['flbmk'] == "N") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
print(round(train_file[(train_file['flbmk'] == "Y") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
print(round(train_file[train_file['flbmk'].isnull() == False]['fraud_ind'].sum()/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
# 在 fraud_ind = 1 的情況下，flbmk = N & flbmk = Y & flbmk = nan 的比例
print(round(train_file[(train_file['flbmk'] == "N") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))
print(round(train_file[(train_file['flbmk'] == "Y") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))
print(round(train_file[train_file['flbmk'].isnull() == True]['fraud_ind'].sum()/train_file[train_file['fraud_ind'] == 1].shape[0], 3))

# 在 fraud_ind = 0 的情況下，flg_3dsmk = N & flg_3dsmk = Y & flg_3dsmk = nan 的比例
print(round(train_file[(train_file['flg_3dsmk'] == "N") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
print(round(train_file[(train_file['flg_3dsmk'] == "Y") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
print(round(train_file[train_file['flg_3dsmk'].isnull() == False]['fraud_ind'].sum()/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
# 在 fraud_ind = 1 的情況下，flg_3dsmk = N & flg_3dsmk = Y & flg_3dsmk = nan 的比例
print(round(train_file[(train_file['flg_3dsmk'] == "N") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))
print(round(train_file[(train_file['flg_3dsmk'] == "Y") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))
print(round(train_file[train_file['flg_3dsmk'].isnull() == True]['fraud_ind'].sum()/train_file[train_file['fraud_ind'] == 1].shape[0], 3))

# 在 fraud_ind = 0 的情況下，insfg = N & insfg = Y 的比例
print(round(train_file[(train_file['insfg'] == "N") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
print(round(train_file[(train_file['insfg'] == "Y") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
# 在 fraud_ind = 1 的情況下，insfg = N & insfg = Y 的比例
print(round(train_file[(train_file['insfg'] == "N") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))
print(round(train_file[(train_file['insfg'] == "Y") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))

# 在 fraud_ind = 0 的情況下，ovrlt = N & ovrlt = Y 的比例
print(round(train_file[(train_file['ovrlt'] == "N") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
print(round(train_file[(train_file['ovrlt'] == "Y") & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
# 在 fraud_ind = 1 的情況下，ovrlt = N & ovrlt = Y 的比例
print(round(train_file[(train_file['ovrlt'] == "N") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))
print(round(train_file[(train_file['ovrlt'] == "Y") & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))

# 將 Y,N 轉換為 1,0
train_file['ecfg'] = (train_file['ecfg']=='Y').astype(int)
train_file['flbmk'] = (train_file['flbmk']=='Y').astype(int)
train_file['flg_3dsmk'] = (train_file['flg_3dsmk']=='Y').astype(int)
train_file['insfg'] = (train_file['insfg']=='Y').astype(int)
train_file['ovrlt'] = (train_file['ovrlt']=='Y').astype(int)

train_file.head()

"""#### 數值型 numeric variables：conam, locdt, loctm (後兩者需要轉換)

##### conam：交易金額-台幣 (經過轉換)
"""

print(len(np.unique(train_file['conam'])))
print(np.unique(train_file['conam']))
print(train_file['conam'].value_counts())
plt.hist(train_file['conam'])
plt.show()

# 交易金額分配
plt.figure(figsize = (18,6))
sns.set_palette('Paired')
plt.suptitle("Boxplot and density distribution of CONAM", fontsize=20)    # 當有使用 plt.subplot，總 title

plt.subplot(1,2,1)
plt.boxplot(train_file['conam'])
plt.subplot(1,2,2)
sns.distplot(train_file['conam']) # 繪製直方密度圖
plt.show() # 顯現圖形

sum(train_file['conam'] == 0)

# 有某種程度的相關性
train_file[(train_file['conam'] == 0) & (train_file['fraud_ind'] == 1)].iloc[:,0:11]

# conam = 0 & conam != 0 其中 Y = 0 與 Y = 1 的比例
print(round(train_file[(train_file['conam'] == 0) & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['conam'] == 0].shape[0], 3))
print(round(train_file[(train_file['conam'] == 0) & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['conam'] == 0].shape[0], 3))
print(round(train_file[(train_file['conam'] != 0) & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['conam'] != 0].shape[0], 3))
print(round(train_file[(train_file['conam'] != 0) & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['conam'] != 0].shape[0], 3))

# 在 fraud_ind = 0 的情況下，conam = 0 & conam != 0 的比例
print(round(train_file[(train_file['conam'] == 0) & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
print(round(train_file[(train_file['conam'] != 0) & (train_file['fraud_ind'] == 0)].shape[0]/train_file[train_file['fraud_ind'] == 0].shape[0], 3))
# 在 fraud_ind = 1 的情況下，conam = 0 & conam != 0 的比例
print(round(train_file[(train_file['conam'] == 0) & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))
print(round(train_file[(train_file['conam'] != 0) & (train_file['fraud_ind'] == 1)].shape[0]/train_file[train_file['fraud_ind'] == 1].shape[0], 3))

# 將金額做 log transformation
train_file['conam_log'] = train_file['conam'].apply(lambda x: math.log(x+1))

print(len(np.unique(train_file['conam_log'])))
print(np.unique(train_file['conam_log']))
print(train_file['conam_log'].value_counts())
plt.hist(train_file['conam_log'])
plt.show()
train_file.boxplot(column='conam_log')
plt.show()

# 將金額做 standardized
mean_c = np.mean(train_file['conam'])
std_c = np.std(train_file['conam'])
train_file['conam_z'] = train_file['conam'].apply(lambda x: (x-mean_c)/std_c)

print(len(np.unique(train_file['conam_z'])))
print(np.unique(train_file['conam_z']))
print(train_file['conam_z'].value_counts())
plt.hist(train_file['conam_z'])
plt.show()
train_file.boxplot(column='conam_z')
plt.show()

"""##### locdt：授權日期"""

print(len(np.unique(train_file['locdt'])))
print(np.unique(train_file['locdt']))
print(train_file['locdt'].value_counts())
sns.set()
sns.countplot(train_file['locdt'])
# plt.hist(train_file['locdt'])
# plt.show()

"""##### loctm：授權時間"""

print(len(np.unique(train_file['loctm'])))
print(np.unique(train_file['loctm']))
print(train_file['loctm'].value_counts())
plt.hist(train_file['loctm'])
plt.show()

"""##### 將 locdt (授權日期) 轉換為星期; loctm(授權時間) 轉換為小時與早中晚"""

# locdt：不需要提
train_file['weekday'] = train_file['locdt'] % 7

print(len(np.unique(train_file['weekday'])))
print(np.unique(train_file['weekday']))
print(train_file['weekday'].value_counts())
sns.set()
sns.countplot(train_file['weekday'])

# loctm
train_file['loctm_hh'] = train_file['loctm'].apply(lambda x: math.floor(x/10000))
train_file['loctm_mm'] = train_file['loctm'].apply(lambda x: math.floor(x/100)-math.floor(x/10000)*100)
train_file['loctm_ss'] = train_file['loctm'].apply(lambda x: math.floor(x)-math.floor(x/100)*100)

print(len(np.unique(train_file['loctm_hh'])))
print(np.unique(train_file['loctm_hh']))
print(train_file['loctm_hh'].value_counts())
sns.set()
sns.countplot(train_file['loctm_hh'])

# loctm_hh - 切割成早中晚
train_file['loctm_0_7'] = train_file['loctm_hh'].apply(lambda x: 1 if ((x >= 0) & (x < 8)) else 0)
train_file['loctm_8_15'] = train_file['loctm_hh'].apply(lambda x: 1 if ((x >= 8) & (x < 16)) else 0)
train_file['loctm_16_23'] = train_file['loctm_hh'].apply(lambda x: 1 if ((x >= 16) & (x <= 23)) else 0)

train_file.head()

"""###### 嘗試將是否盜刷的紀錄放在同一張表中"""

df0 = train_file[train_file['fraud_ind'] == 0]
df1 = train_file[train_file['fraud_ind'] == 1]

plt.hist([df0.weekday, df1.weekday], label = ['Normal', 'Fraud'], stacked = True)
plt.legend()
plt.show()

# 正常交易中的星期分布
sns.set()
sns.set_palette('Paired')
sns.countplot(df0.weekday)

# 盜刷交易中的星期分布
sns.set()
sns.set_palette('Paired')
sns.countplot(df1.weekday)

plt.hist([df0.loctm_hh, df1.loctm_hh], label = ['Normal', 'Fraud'], stacked = True)
plt.legend()
plt.show()

# 正常交易中的時間(小時)分布
sns.set()
sns.set_palette('Paired')
sns.countplot(df0.loctm_hh)

sns.set()
sns.set_palette('Paired')
sns.countplot(df1.loctm_hh)

train_file_sp = train_file.iloc[:,[0,1,2,4,5,6,7,8,9,10,11,12,13,16,17,18,19,20,21]]
import scipy.stats
spearman_corr = scipy.stats.spearmanr(train_file_sp)

print(train_file_sp.columns)
print(train_file_sp.shape)
train_file_sp.head()

spearman_corr1 = pd.DataFrame(np.array(spearman_corr)[1],index= ['acqic', 'bacno', 'cano', 'contp', 'csmcu', 'ecfg', 'etymd', 'flbmk','flg_3dsmk', 'fraud_ind', 'hcefg', 'insfg', 'iterm', 'mcc', 'mchno','ovrlt', 'scity', 'stocn', 'stscd'], columns = ['acqic', 'bacno', 'cano', 'contp', 'csmcu', 'ecfg', 'etymd', 'flbmk','flg_3dsmk', 'fraud_ind', 'hcefg', 'insfg', 'iterm', 'mcc', 'mchno','ovrlt', 'scity', 'stocn', 'stscd'])
for i in range(0,19):
    spearman_corr1.iloc[:,i] = spearman_corr1.iloc[:,i].apply(lambda x: round(x,3))
spearman_corr1

"""## 卡號跟凌晨刷卡(看特性)"""

fig, ax = plt.subplots(figsize = (20,15))
seaborn.heatmap(spearman_corr1, center = 0, annot = True, cmap="YlGnBu", )
mp.show()

"""##### 將類別變數改成dummy：acqic, bacno, cano, contp, csmcu, etymd, hcefg, mcc, mchno, scity, stocn, stscd"""

train_file.head()

# 其他被註解掉的則是因為類別數太多，等等直接pd.get_dunnies會跑不動(RAM不夠)
#train_file['acqic'] = train_file['acqic'].astype(str)
#train_file['bacno'] = train_file['bacno'].astype(str)
#train_file['cano'] = train_file['cano'].astype(str)
train_file['contp'] = train_file['contp'].astype(str)
train_file['csmcu'] = train_file['csmcu'].astype(str)
train_file['ecfg'] = train_file['ecfg'].astype(str)
train_file['etymd'] = train_file['etymd'].astype(str)
train_file['flbmk'] = train_file['flbmk'].astype(str)
train_file['flg_3dsmk'] = train_file['flg_3dsmk'].astype(str)
train_file['hcefg'] = train_file['hcefg'].astype(str)
train_file['insfg'] = train_file['insfg'].astype(str)
train_file['iterm'] = train_file['iterm'].astype(str)
#train_file['mcc'] = train_file['mcc'].astype(str)
#train_file['mchno'] = train_file['mchno'].astype(str)
train_file['ovrlt'] = train_file['ovrlt'].astype(str)
#train_file['scity'] = train_file['scity'].astype(str)
train_file['stocn'] = train_file['stocn'].astype(str)
train_file['stscd'] = train_file['stscd'].astype(str)

train_file.dtypes

train_file_dummies = pd.get_dummies(train_file)
pd.DataFrame(train_file_dummies)

train = pd.read_csv('/content/gdrive/My Drive/Colab/FinTech/data/train_freq.csv')

# 為了畫圖方便用
train['Period'] = train['loctm_hour'].apply(lambda x: 'Early Morning(0-7)' if ((x >= 0) & (x < 8)) else ('Daytime(8-15)' if ((x >= 8) & (x < 16)) else 'Night(16-23)'))

print(len(np.unique(train['freq_bacno'])))
print(np.unique(train['freq_bacno']))
print(train['freq_bacno'].value_counts())
# sns.set()
# sns.countplot(train['freq_bacno'])

print(len(np.unique(train['freq_cano'])))
print(np.unique(train['freq_cano']))
print(train['freq_cano'].value_counts())
# sns.set()
# sns.countplot(train['freq_cano'])

df0 = train[train['fraud_ind'] == 0]
df1 = train[train['fraud_ind'] == 1]

print(round(df0['Period'].value_counts()/df0.shape[0], 3))
print(round(df1['Period'].value_counts()/df1.shape[0], 3))

# 早中晚分布：非盜刷 vs. 盜刷
# category = ["Morning", "Afternoon", "Night"] # 總類名稱
print(df0['Period'].value_counts())
print(df1['Period'].value_counts())

plt.figure(figsize = (12,6))
plt.suptitle('Histogram of Period', fontsize=20)    # 當有使用 plt.subplot，總 title
sns.set()
plt.subplot(1,2,1)
plt.title('Normal Transaction')
sns.countplot(df0['Period'], color = "#3498db", order = df0['Period'].value_counts().index)
plt.subplot(1,2,2)
plt.title('Fraud Transaction')
sns.countplot(df1['Period'], color = 'orange', order = df0['Period'].value_counts().index)

# freq_bacno分布：非盜刷 vs. 盜刷
plt.figure(figsize = (18,6))
plt.suptitle('Histogram of Frequency of BACNO', fontsize=20)    # 當有使用 plt.subplot，總 title
sns.set()
plt.subplot(1,2,1)
plt.title('Normal Transaction')
sns.countplot(df0['freq_bacno'], color = "#3498db")
plt.subplot(1,2,2)
plt.title('Fraud Transaction')
sns.countplot(df1['freq_bacno'], color = 'orange')

# freq_cano分布：非盜刷 vs. 盜刷
plt.figure(figsize = (18,6))
plt.suptitle('Histogram of Frequency of CANO', fontsize=20)    # 當有使用 plt.subplot，總 title
sns.set()
plt.subplot(1,2,1)
plt.title('Normal Transaction')
sns.countplot(df0['freq_cano'], color = "#3498db")
plt.subplot(1,2,2)
plt.title('Fraud Transaction')
sns.countplot(df1['freq_cano'], color = 'orange')

# 這個畫出來結果太差，不採用
sns.set()
sns.countplot(x = 'freq_cano', hue = 'fraud_ind', data = train, )
plt.legend(loc='upper right')

"""## 錯誤案例分析"""

pred = pd.read_csv('/content/gdrive/My Drive/Colab/FinTech/data/test_withPred.csv')

pred.head()

from sklearn.metrics import confusion_matrix

tn, fp, fn, tp = confusion_matrix(pred['fraud_ind'], pred['predict']).ravel()
print(tn, fp, fn, tp)

TP = pred[(pred['fraud_ind'] == 1) & (pred['predict'] == 1)]  # tp
FP = pred[(pred['fraud_ind'] == 0) & (pred['predict'] == 1)]  # fp
FN = pred[(pred['fraud_ind'] == 1) & (pred['predict'] == 0)]  # fn
TN = pred[(pred['fraud_ind'] == 0) & (pred['predict'] == 0)]  # tn

pred['cMat'] = ""
for i in range(pred.shape[0]):
  if (pred['fraud_ind'][i] == 1) & (pred['predict'][i] == 1):
    pred['cMat'][i] = 'TP'
  elif (pred['fraud_ind'][i] == 0) & (pred['predict'][i] == 1):
    pred['cMat'][i] = 'FP'
  elif (pred['fraud_ind'][i] == 1) & (pred['predict'][i] == 0):
    pred['cMat'][i] = 'FN'
  elif (pred['fraud_ind'][i] == 0) & (pred['predict'][i] == 0):
    pred['cMat'][i] = 'TN'

Result3 = '/content/gdrive/My Drive/Colab/FinTech/data/test_withPred_cMat.csv'
pred.to_csv(Result3, index = False)

print(len(np.unique(pred['cMat'])))
print(np.unique(pred['cMat']))
print(pred['cMat'].value_counts())
sns.set()
sns.countplot(pred['cMat'])

pred.boxplot(column='conam')
plt.show()

plt.title("Boxplot of conam") # 圖的標題
sns.set_palette('Paired')
sns.boxplot(x = "cMat", y = "conam", data = pred)  # 繪製盒狀圖
#sns.boxplot(x="day",y="total_bill",hue="sex",data=df) # 繪製盒狀圖
plt.show() # 顯現圖形

# ecfg分布：confusion matrix
print(TN['ecfg'].value_counts())
print(TP['ecfg'].value_counts())
print(FP['ecfg'].value_counts())
print(FN['ecfg'].value_counts())

plt.figure(figsize = (12,12))
sns.set_palette('Paired')
plt.suptitle('Analysis of ECFG', fontsize=20)    # 當有使用 plt.subplot，總 title

plt.subplot(2,2,1)
plt.title('The distribution of ecfg for True Negative') 
sns.countplot(TN["ecfg"])
plt.subplot(2,2,2)
plt.title('The distribution of ecfg for True Positive') 
sns.countplot(TP["ecfg"])
plt.subplot(2,2,3)
plt.title('The distribution of ecfg for False Positive') 
sns.countplot(FP["ecfg"])
plt.subplot(2,2,4)
plt.title('The distribution of ecfg for False Negative') 
sns.countplot(FN["ecfg"])
plt.show()
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Analysis of ECFG.png")

# flbmk分布：confusion matrix
print(TN['flbmk'].value_counts())
print(TP['flbmk'].value_counts())
print(FP['flbmk'].value_counts())
print(FN['flbmk'].value_counts())
plt.figure(figsize = (12,12))
sns.set_palette('Paired')
plt.suptitle('Analysis of FLBMK', fontsize=20)    # 當有使用 plt.subplot，總 title

plt.subplot(2,2,1)
plt.title('The distribution of flbmk for True Negative') 
sns.countplot(TN["flbmk"])
plt.subplot(2,2,2)
plt.title('The distribution of flbmk for True Positive') 
sns.countplot(TP["flbmk"])
plt.subplot(2,2,3)
plt.title('The distribution of flbmk for False Positive') 
sns.countplot(FP["flbmk"])
plt.subplot(2,2,4)
plt.title('The distribution of flbmk for False Negative') 
sns.countplot(FN["flbmk"])
plt.show()
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Analysis of FLBMK.png")

# flg_3dsmk分布：confusion matrix
print(TN['flbmk'].value_counts())
print(TP['flbmk'].value_counts())
print(FP['flbmk'].value_counts())
print(FN['flbmk'].value_counts())
plt.figure(figsize = (12,12))
sns.set_palette('Paired')
plt.suptitle('Analysis of FLG_3DSMK', fontsize=20)    # 當有使用 plt.subplot，總 title

plt.subplot(2,2,1)
plt.title('The distribution of flg_3dsmk for True Negative') 
sns.countplot(TN["flg_3dsmk"])
plt.subplot(2,2,2)
plt.title('The distribution of flg_3dsmk for True Positive') 
sns.countplot(TP["flg_3dsmk"])
plt.subplot(2,2,3)
plt.title('The distribution of flg_3dsmk for False Positive') 
sns.countplot(FP["flg_3dsmk"])
plt.subplot(2,2,4)
plt.title('The distribution of flg_3dsmk for False Negative') 
sns.countplot(FN["flg_3dsmk"])
plt.show()
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Analysis of FLG_3DSMK.png")

# insfg分布：confusion matrix
print(TN['insfg'].value_counts())
print(TP['insfg'].value_counts())
print(FP['insfg'].value_counts())
print(FN['insfg'].value_counts())
plt.figure(figsize = (12,12))
sns.set_palette('Paired')
plt.suptitle('Analysis of INSFG', fontsize=20)    # 當有使用 plt.subplot，總 title

plt.subplot(2,2,1)
plt.title('The distribution of insfg for True Negative') 
sns.countplot(TN["insfg"])
plt.subplot(2,2,2)
plt.title('The distribution of insfg for True Positive') 
sns.countplot(TP["insfg"])
plt.subplot(2,2,3)
plt.title('The distribution of insfg for False Positive') 
sns.countplot(FP["insfg"])
plt.subplot(2,2,4)
plt.title('The distribution of insfg for False Negative') 
sns.countplot(FN["insfg"])
plt.show()
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Analysis of INSFG.png")

# ovrlt分布：confusion matrix
print(TN['ovrlt'].value_counts())
print(TP['ovrlt'].value_counts())
print(FP['ovrlt'].value_counts())
print(FN['ovrlt'].value_counts())
plt.figure(figsize = (12,12))
sns.set_palette('Paired')
plt.suptitle('Analysis of OVRLT', fontsize=20)    # 當有使用 plt.subplot，總 title

plt.subplot(2,2,1)
plt.title('The distribution of ovrlt for True Negative') 
sns.countplot(TN["ovrlt"])
plt.subplot(2,2,2)
plt.title('The distribution of ovrlt for True Positive') 
sns.countplot(TP["ovrlt"])
plt.subplot(2,2,3)
plt.title('The distribution of ovrlt for False Positive') 
sns.countplot(FP["ovrlt"])
plt.subplot(2,2,4)
plt.title('The distribution of ovrlt for False Negative') 
sns.countplot(FN["ovrlt"])
plt.show()
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Analysis of OVRLT.png")

plt.figure(figsize = (8,8))
plt.title('Boxplot analysis for Frequency of BACNO', fontsize = 15) # 圖的標題
sns.boxplot(x = "cMat", y = "freq_bacno", data = pred) # 繪製計數圖
plt.show() # 顯現圖形 
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Boxplot analysis for Frequency of BACNO.png")

plt.figure(figsize = (8,8))
plt.title('Boxplot analysis for Frequency of CANO', fontsize = 15) # 圖的標題
sns.boxplot(x = "cMat", y = "freq_cano", data = pred) # 繪製計數圖
plt.show() # 顯現圖形 
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Boxplot analysis for Frequency of CANO.png")

# freq_bacno分布：confusion matrix
plt.figure(figsize = (20,12))
sns.set_palette('Paired')
plt.suptitle('Analysis of Frequency of BACNO', fontsize=20)     # 當有使用 plt.subplot，總 title

plt.subplot(2,2,1)
plt.title('The distribution of freq_bacno for True Negative') 
sns.countplot(TN["freq_bacno"])
plt.subplot(2,2,2)
plt.title('The distribution of freq_bacno for True Positive') 
sns.countplot(TP["freq_bacno"])
plt.subplot(2,2,3)
plt.title('The distribution of freq_bacno for False Positive') 
sns.countplot(FP["freq_bacno"])
plt.subplot(2,2,4)
plt.title('The distribution of freq_bacno for False Negative') 
sns.countplot(FN["freq_bacno"])
plt.show()
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Analysis of Frequency of BACNO.png")

# freq_cano分布：confusion matrix
plt.figure(figsize = (20,12))
sns.set_palette('Paired')
plt.suptitle('Analysis of Frequency of CANO', fontsize=20)    # 當有使用 plt.subplot，總 title

plt.subplot(2,2,1)
plt.title('The distribution of freq_cano for True Negative') 
sns.countplot(TN["freq_cano"])
plt.subplot(2,2,2)
plt.title('The distribution of freq_cano for True Positive') 
sns.countplot(TP["freq_cano"])
plt.subplot(2,2,3)
plt.title('The distribution of freq_cano for False Positive') 
sns.countplot(FP["freq_cano"])
plt.subplot(2,2,4)
plt.title('The distribution of freq_cano for False Negative') 
sns.countplot(FN["freq_cano"])
plt.show()
plt.savefig("/content/gdrive/My Drive/Colab/FinTech/figure/Analysis of Frequency of CANO.png")

train = pd.read_csv('/content/gdrive/My Drive/Colab/FinTech/data/train_freq.csv')
test = pd.read_csv('/content/gdrive/My Drive/Colab/FinTech/data/test_freq.csv')

import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = '  缺失值', '無缺失值', 'Dogs', 'Logs'
sizes = [0.824, 100-0.824]
explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
labels = ['fraud','normal']  
fig1, ax1 = plt.subplots()
ax1.pie(sizes,labels=labels, explode=explode, autopct='%1.3f%%',shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Pie chart of Missing Value over All Transaction", {"fontsize" : 18})
plt.legend(loc = "best")
plt.show()

import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = '  缺失值', '無缺失值', 'Dogs', 'Logs'
sizes = [1.021, 100-1.021]
explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
labels = ['fraud','normal']  
fig1, ax1 = plt.subplots()
ax1.pie(sizes,labels=labels, explode=explode, autopct='%1.3f%%',shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Pie chart of Missing Value over Fraud Transaction", {"fontsize" : 18})
plt.legend(loc = "best")
plt.show()