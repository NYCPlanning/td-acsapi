#%% Settings
import requests
import pandas as pd
import numpy as np
import geopandas as gpd


pd.set_option('display.max_columns', None)
path='C:/Users/mayij/Desktop/DOC/'
path='C:/Users/Y_Ma2/Desktop/'

apikey=pd.read_csv(path+'GITHUB/td-acsapi/secrets.csv',dtype=str).loc[0,'value']
usernm=pd.read_csv(path+'GITHUB/td-acsapi/secrets.csv',dtype=str).loc[1,'value']
passwd=pd.read_csv(path+'GITHUB/td-acsapi/secrets.csv',dtype=str).loc[2,'value']

p={'http':'http://'+str(usernm)+':'+str(passwd)+'@dcpproxy1.dcp.nycnet:8080',
   'https':'http://'+str(usernm)+':'+str(passwd)+'@dcpproxy1.dcp.nycnet:8080'}



#%% County list
tp=[]
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george']:
    k=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv')
    k['county']=[str(x)[0:5] for x in k['tractid']]
    k=k['county'].unique()
    tp=tp+list(k)
tp=set(tp)



#%% All Locations
df=pd.DataFrame()
quadstatectclipped=gpd.read_file(path+'Blueprint/travelshed/quadstatectclipped.geojson')
for i in ['dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp=tp[['tractid']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df=df.drop_duplicates(keep='first').reset_index(drop=True)
df.to_csv(path+'Blueprint/travelshed/all/all.csv',index=False)
df=pd.merge(quadstatectclipped,df,how='inner',on='tractid')
df.to_file(path+'Blueprint/travelshed/all/all.geojson',driver='GeoJSON')



#%% Population
df=pd.DataFrame()
for i in ['005','047','059','061','081','085','119']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/profile?get=group(DP05)&for=tract:*&in=state:36 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','DP05_0001E','DP05_0020E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
for i in ['003','017','031']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/profile?get=group(DP05)&for=tract:*&in=state:34 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','DP05_0001E','DP05_0020E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.columns=['tractid','totalpop','pop16']
df.to_csv(path+'Blueprint/census/pop.csv',index=False)

df=pd.DataFrame()
pop=pd.read_csv(path+'Blueprint/census/pop.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp=pd.merge(tp,pop,how='left',on='tractid')
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'totalpop':'sum','pop16':'sum'}).reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/popsumregion.csv',index=False)

df=pd.DataFrame()
pop=pd.read_csv(path+'Blueprint/census/pop.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp['county']=[str(x)[0:5] for x in tp['tractid']]
    tp=tp[np.isin(tp['county'],['36005','36047','36061','36081','36085'])].reset_index(drop=True)
    tp=pd.merge(tp,pop,how='left',on='tractid')
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'totalpop':'sum','pop16':'sum'}).reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/popsumnyc.csv',index=False)



#%% Race
df=pd.DataFrame()
for i in ['005','047','059','061','081','085','119']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/profile?get=group(DP05)&for=tract:*&in=state:36 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','DP05_0071E','DP05_0076E','DP05_0077E','DP05_0078E','DP05_0079E','DP05_0080E','DP05_0081E','DP05_0082E','DP05_0083E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
for i in ['003','017','031']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/profile?get=group(DP05)&for=tract:*&in=state:34 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','DP05_0071E','DP05_0076E','DP05_0077E','DP05_0078E','DP05_0079E','DP05_0080E','DP05_0081E','DP05_0082E','DP05_0083E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.columns=['tractid','hispanic','nonhisp','white','black','native','asian','pacific','other','two']
df.to_csv(path+'Blueprint/census/race.csv',index=False)

df=pd.DataFrame()
race=pd.read_csv(path+'Blueprint/census/race.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp['county']=[str(x)[0:5] for x in tp['tractid']]
    tp=tp[np.isin(tp['county'],['36005','36047','36061','36081','36085'])].reset_index(drop=True)
    tp=pd.merge(tp,race,how='left',on='tractid')
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'hispanic':'sum','nonhisp':'sum','white':'sum','black':'sum',
                                                    'native':'sum','asian':'sum','pacific':'sum',
                                                    'other':'sum','two':'sum'}).reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/racesum.csv',index=False)



#%% Education
df=pd.DataFrame()
for i in ['005','047','059','061','081','085','119']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/subject?get=NAME,group(S1501)&for=tract:*&in=state:36 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','S1501_C01_006E','S1501_C01_007E','S1501_C01_008E','S1501_C01_009E','S1501_C01_010E','S1501_C01_011E','S1501_C01_012E','S1501_C01_013E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
for i in ['003','017','031']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/subject?get=NAME,group(S1501)&for=tract:*&in=state:34 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','S1501_C01_006E','S1501_C01_007E','S1501_C01_008E','S1501_C01_009E','S1501_C01_010E','S1501_C01_011E','S1501_C01_012E','S1501_C01_013E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.columns=['tractid','pop25','lt9grade','912grade','high','college','associate','bachelor','graduate']
df.to_csv(path+'Blueprint/census/edu.csv',index=False)

df=pd.DataFrame()
edu=pd.read_csv(path+'Blueprint/census/edu.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp['county']=[str(x)[0:5] for x in tp['tractid']]
    tp=tp[np.isin(tp['county'],['36005','36047','36061','36081','36085'])].reset_index(drop=True)
    tp=pd.merge(tp,edu,how='left',on='tractid')
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'pop25':'sum','lt9grade':'sum','912grade':'sum','high':'sum',
                                                    'college':'sum','associate':'sum','bachelor':'sum',
                                                    'graduate':'sum'}).reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/edusum.csv',index=False)



#%% Household Income
df=pd.DataFrame()
for i in ['005','047','059','061','081','085','119']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5?get=NAME,group(B19001)&for=tract:*&in=state:36 county:'+str(i)+'&key='+apikey,proxies=p)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','B19001_001E','B19001_002E','B19001_003E','B19001_004E','B19001_005E','B19001_006E','B19001_007E','B19001_008E','B19001_009E','B19001_010E','B19001_011E','B19001_012E','B19001_013E','B19001_014E','B19001_015E','B19001_016E','B19001_017E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
for i in ['003','017','031']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5?get=NAME,group(B19001)&for=tract:*&in=state:34 county:'+str(i)+'&key='+apikey,proxies=p)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','B19001_001E','B19001_002E','B19001_003E','B19001_004E','B19001_005E','B19001_006E','B19001_007E','B19001_008E','B19001_009E','B19001_010E','B19001_011E','B19001_012E','B19001_013E','B19001_014E','B19001_015E','B19001_016E','B19001_017E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.columns=['tractid','hh','lt10','lt15','lt20','lt25','lt30','lt35','lt40','lt45','lt50','lt60','lt75','lt100','lt125','lt150','lt200','mt200']
df.to_csv(path+'Blueprint/census/hhinc.csv',index=False)

df=pd.DataFrame()
hhinc=pd.read_csv(path+'Blueprint/census/hhinc.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp['county']=[str(x)[0:5] for x in tp['tractid']]
    tp=tp[np.isin(tp['county'],['36005','36047','36061','36081','36085'])].reset_index(drop=True)
    tp=pd.merge(tp,hhinc,how='left',on='tractid')
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'hh':'sum','lt10':'sum','lt15':'sum','lt20':'sum','lt25':'sum',
                                                    'lt30':'sum','lt35':'sum','lt40':'sum','lt45':'sum','lt50':'sum',
                                                    'lt60':'sum','lt75':'sum','lt100':'sum','lt125':'sum',
                                                    'lt150':'sum','lt200':'sum','mt200':'sum'}).reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/hhincsum.csv',index=False)



#%% Poverty
df=pd.DataFrame()
for i in ['005','047','059','061','081','085','119']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/subject?get=NAME,group(S1701)&for=tract:*&in=state:36 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','S1701_C01_001E','S1701_C02_001E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
for i in ['003','017','031']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/subject?get=NAME,group(S1701)&for=tract:*&in=state:34 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','S1701_C01_001E','S1701_C02_001E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.columns=['tractid','popdet','poverty']
df.to_csv(path+'Blueprint/census/poverty.csv',index=False)

df=pd.DataFrame()
poverty=pd.read_csv(path+'Blueprint/census/poverty.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp['county']=[str(x)[0:5] for x in tp['tractid']]
    tp=tp[np.isin(tp['county'],['36005','36047','36061','36081','36085'])].reset_index(drop=True)
    tp=pd.merge(tp,poverty,how='left',on='tractid')
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'popdet':'sum','poverty':'sum'}).reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/povertysum.csv',index=False)



#%% Mode
df=pd.DataFrame()
for i in ['005','047','059','061','081','085','119']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5?get=NAME,group(B08301)&for=tract:*&in=state:36 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','B08301_001E','B08301_003E','B08301_004E','B08301_011E','B08301_012E','B08301_013E','B08301_014E','B08301_015E','B08301_016E','B08301_017E','B08301_018E','B08301_019E','B08301_020E','B08301_021E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
for i in ['003','017','031']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5?get=NAME,group(B08301)&for=tract:*&in=state:34 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','B08301_001E','B08301_003E','B08301_004E','B08301_011E','B08301_012E','B08301_013E','B08301_014E','B08301_015E','B08301_016E','B08301_017E','B08301_018E','B08301_019E','B08301_020E','B08301_021E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.columns=['tractid','worker16','drivealone','carpool','bus','subway','rail','streetcar','ferry','taxi','motor','bike','walk','other','home']
df.to_csv(path+'Blueprint/census/mode.csv',index=False)

df=pd.DataFrame()
mode=pd.read_csv(path+'Blueprint/census/mode.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp['county']=[str(x)[0:5] for x in tp['tractid']]
    tp=tp[np.isin(tp['county'],['36005','36047','36061','36081','36085'])].reset_index(drop=True)
    tp=pd.merge(tp,mode,how='left',on='tractid')
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'worker16':'sum','drivealone':'sum','carpool':'sum',
                                                    'bus':'sum','subway':'sum','rail':'sum','streetcar':'sum',
                                                    'ferry':'sum','taxi':'sum','motor':'sum','bike':'sum',
                                                    'walk':'sum','other':'sum','home':'sum'}).reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/modesum.csv',index=False)



#%% Time
df=pd.DataFrame()
for i in ['005','047','059','061','081','085','119']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5?get=NAME,group(B08303)&for=tract:*&in=state:36 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','B08303_001E','B08303_002E','B08303_003E','B08303_004E','B08303_005E','B08303_006E','B08303_007E','B08303_008E','B08303_009E','B08303_010E','B08303_011E','B08303_012E','B08303_013E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
for i in ['003','017','031']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5?get=NAME,group(B08303)&for=tract:*&in=state:34 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','B08303_001E','B08303_002E','B08303_003E','B08303_004E','B08303_005E','B08303_006E','B08303_007E','B08303_008E','B08303_009E','B08303_010E','B08303_011E','B08303_012E','B08303_013E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.columns=['tractid','nonhome','lt5','t59','t1014','t1519','t2024','t2529','t3034','t3539','t4044','t4559','t6089','lt90']
df.to_csv(path+'Blueprint/census/time.csv',index=False)

df=pd.DataFrame()
time=pd.read_csv(path+'Blueprint/census/time.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp['county']=[str(x)[0:5] for x in tp['tractid']]
    tp=tp[np.isin(tp['county'],['36005','36047','36061','36081','36085'])].reset_index(drop=True)
    tp=pd.merge(tp,time,how='left',on='tractid')
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'nonhome':'sum','lt5':'sum','t59':'sum','t1014':'sum',
                                                    't1519':'sum','t2024':'sum','t2529':'sum','t3034':'sum',
                                                    't3539':'sum','t4044':'sum','t4559':'sum','t6089':'sum',
                                                    'lt90':'sum'}).reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/timesum.csv',index=False)



#%% Mean Time
df=pd.DataFrame()
for i in ['005','047','059','061','081','085','119']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/subject?get=NAME,group(S0801)&for=tract:*&in=state:36 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','S0801_C02_046E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
for i in ['003','017','031']:
    rs=requests.get('https://api.census.gov/data/2019/acs/acs5/subject?get=NAME,group(S0801)&for=tract:*&in=state:34 county:'+str(i)+'&key='+apikey)
    tp=pd.read_json(rs.content)
    tp.columns=tp.loc[0]
    tp['tractid']=[str(x)[9:] for x in tp['GEO_ID']]
    tp=tp.loc[1:,['tractid','S0801_C02_046E']].reset_index(drop=True)
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.columns=['tractid','meantime']
df.to_csv(path+'Blueprint/census/meantime.csv',index=False)

df=pd.DataFrame()
mode=pd.read_csv(path+'Blueprint/census/mode.csv',dtype=float,converters={'tractid':str})
meantime=pd.read_csv(path+'Blueprint/census/meantime.csv',dtype=float,converters={'tractid':str})
for i in ['times square','dbk','broadway junction','bxhub','fordham','morris park','e14st','e23st','e125st','w125st','lic','jamaica','st george','all']:
    tp=pd.read_csv(path+'Blueprint/travelshed/'+str(i)+'/'+str(i)+'.csv',dtype=str)
    tp['county']=[str(x)[0:5] for x in tp['tractid']]
    tp=tp[np.isin(tp['county'],['36005','36047','36061','36081','36085'])].reset_index(drop=True)
    tp=pd.merge(tp,mode,how='left',on='tractid')
    tp=pd.merge(tp,meantime,how='left',on='tractid')
    tp=tp[tp['meantime']>=0].reset_index(drop=True)
    tp['aggtime']=tp['worker16']*tp['meantime']
    tp['location']=str(i)
    tp=tp.groupby(['location'],as_index=False).agg({'aggtime':'sum','worker16':'sum','home':'sum'}).reset_index(drop=True)
    tp['meantime']=tp['aggtime']/(tp['worker16']-tp['home'])
    df=pd.concat([df,tp],axis=0,ignore_index=True)
df.to_csv(path+'Blueprint/census/meantimesum.csv',index=False)





