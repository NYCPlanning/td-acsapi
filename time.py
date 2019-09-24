import requests
import pandas as pd

apikey=pd.read_csv('/home/jovyan/apikey.txt',header=None)

ct=['36005028700','36005030100','36005040701','36005042300','36005042902','36005043400','36005027700','36005042000','36005042901',
    '36005027900','36005034300','36005034500','36005033700','36005040702','36005035100','36005043100','36005041400','36005044200',
    '36005044400','36005040900','36005042100','36005044901','36005044902','36005041100','36005029301','36005028100','36005045102',
    '36005030701','36005031900','36005045101','36005041800','36005029700','36005030900','36005032300','36005043500','36005029302',
    '36005028500','36005029500','36005033500','36005028300','36005028900','36005041300','36005041900','36005041500','36005042500',
    '36005033400']
ct=['36005036000','36005036800','36005037000','36005037200','36005039200','36005039400','36005039600','36005039800','36005040400'
    ,'36005040600','36005042200','36005042400','36005042800','36005043000','36005043400','36005043600','36005034000','36005044800',
    '36005034200','36005034400','36005042000','36005040800','36005030200','36005038200','36005038800','36005039000','36005038600',
    '36005042600','36005035800','36005045600','36005037400','36005035000','36005045800','36005046000','36005038000','36005037600',
    '36005034800','36005036400','36005044200','36005044400','36005037800','36005043500','36005048400','36005046201','36005035600',
    '36005046202','36005033400']

# Aggregate Travel Time
df=pd.DataFrame(index=ct,columns=['001E'])
rs=requests.get('https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B08013)&for=tract:*&in=state:36 county:005&key='+apikey).json()
rs=pd.DataFrame(rs)
rs.columns=rs.loc[0]
rs=rs.loc[1:].set_index('GEO_ID')
for i in df.index:
    for j in df.columns:
        df.loc[i,j]=pd.to_numeric(rs.loc['1400000US'+i,'B08013_'+j])
df.columns=['TOTALTT']
df.loc['STUDY AREA']=df.sum(axis=0)
aggtt=df.loc['STUDY AREA','TOTALTT']

# Total Non-Home Workers
df=pd.DataFrame(index=ct,columns=['001E','003E','005E','006E','007E','008E','009E','011E','012E','013E','014E','015E','016E','017E','018E','019E','020E','021E'])
rs=requests.get('https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B08301)&for=tract:*&in=state:36 county:005&key='+apikey).json()
rs=pd.DataFrame(rs)
rs.columns=rs.loc[0]
rs=rs.loc[1:].set_index('GEO_ID')
for i in df.index:
    for j in df.columns:
        df.loc[i,j]=pd.to_numeric(rs.loc['1400000US'+i,'B08301_'+j])
df.columns=['TOTAL','CAR1','CAR2','CAR3','CAR4','CAR56','CAR7+','BUS','STREETCAR','SUBWAY','RAILROAD','FERRY','TAXI','MOTORCYCLE','BICYCLE','WALKED','OTHER','HOME']
df.loc['STUDY AREA']=df.sum(axis=0)
nonhome=df.loc['STUDY AREA','TOTAL']-df.loc['STUDY AREA','HOME']
avgtt=aggtt/nonhome

# Detailed Travel Time
df=pd.DataFrame(index=ct,columns=['001E','002E','003E','004E','005E','006E','007E','008E','009E','010E','011E','012E','013E'])
rs=requests.get('https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B08303)&for=tract:*&in=state:36 county:005&key='+apikey).json()
rs=pd.DataFrame(rs)
rs.columns=rs.loc[0]
rs=rs.loc[1:].set_index('GEO_ID')
for i in df.index:
    for j in df.columns:
        df.loc[i,j]=pd.to_numeric(rs.loc['1400000US'+i,'B08303_'+j])
df.columns=['TOTAL','<5','5~9','10~14','15~19','20~24','25~29','30~34','35~39','40~44','45~59','60~89','>=90']
df.loc['STUDY AREA']=df.sum(axis=0)
