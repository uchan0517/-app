#天気予報
import datetime
import requests
from bs4 import BeautifulSoup
import json
import re
import streamlit as st
import os
import pandas as pd

dt_now=datetime.datetime.now()

# 気象庁データの取得

city_code=270000
jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{city_code}.json"
jma_json = requests.get(jma_url).json()
print(jma_json)

# 取得したいデータを選ぶ
jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]#今の日時
jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]#今日の天気
jma_temps = jma_json[0]["timeSeries"][2]["areas"][0]["temps"][0]#明日最低気温
jma_temps2 = jma_json[0]["timeSeries"][2]["areas"][0]["temps"][1]#明日最高気温
jma_temps_1 = jma_json[1]["timeSeries"][1]["areas"][0]["tempsMin"][1]#明後日最低気温
jma_temps2_2 = jma_json[1]["timeSeries"][1]["areas"][0]["tempsMax"][1]#明後日最高気温
jma_temps_3 = jma_json[1]["timeSeries"][1]["areas"][0]["tempsMin"][2]#明後日2最低気温
jma_temps2_4 = jma_json[1]["timeSeries"][1]["areas"][0]["tempsMax"][2]#明後日2最高気温
jma_pops = jma_json[0]["timeSeries"][1]["areas"][0]["pops"][1]#午前六時の降水確率
jma_pops2 = jma_json[0]["timeSeries"][1]["areas"][0]["pops"][2]#午後六時の降水確率

week=['月','火','水','木','金','土','日']


#jma_rainfall = jma_json["Feature"][0]["Property"]["WeatherList"]["Weather"][0]["Rainfall"]
# 全角スペースの削除
jma_weather = jma_weather.replace('　', '')
print(jma_date)
print(jma_weather)
print(jma_temps_1)
print(jma_temps2_2)
print(jma_pops)
print(jma_pops2)
#print(jma_rainfall)
time=[]
time_2=[]
temps=[]
temps_2=[]
pops=[]
pops_2=[]
i=[]

length = len(jma_json[0]["timeSeries"][0]["timeDefines"])
for i in range(length):
    time.append(jma_json[0]["timeSeries"][0]["timeDefines"][i])
    time_2.append(jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][i])
for i in range(2):
    temps.append(jma_json[0]["timeSeries"][2]["areas"][0]["temps"][i])
for i in range(5):
    pops.append(jma_json[0]["timeSeries"][1]["areas"][0]["pops"][i])
#print(time)
#print(time_2)
#print(temps)
#print(pops)

png=os.listdir('image')
print(png)



if length == 3:
    data_list = [[time[0],time[1],time[2]],
        [time_2[0],time_2[1],time_2[2]]]
else:
    data_list = [[time[0],time[1]],
        [time_2[0],time_2[1]]]
df = pd.DataFrame( data_list )

#print(df)


days_date=[]
threedays_date2=[]
threedays_date=[]
threedays_weather=[]
pattern=r'(\d{1,2})-(\d{1,2})T'
pattern2=r'(\d{1,2})-(\d{1,2})T(\d{1,2}):(\d{1,2})'
for i in range(length):
    date=re.findall(pattern,jma_json[0]["timeSeries"][0]["timeDefines"][i])
    for month, day in date:
        days_date.append(f"{month.zfill(2)}/{day.zfill(2)}")
        threedays_date.append(f"{month.zfill(2)}/{day.zfill(2)}({week[dt_now.weekday()+i]})")

for i in range (5):
    date=re.findall(pattern2,jma_json[0]["timeSeries"][1]["timeDefines"][i])
    for month, day, time2,time2_2 in date:
        threedays_date2.append(f"{month.zfill(2)}/{day.zfill(2)}   {time2.zfill(2)}:{time2_2.zfill(2)}")
    

#print (threedays_date)
st.title("weather report")    




    
col1,col2,col3=st.columns(3)
with col1:
    st.header(threedays_date[0])
    st.write(time_2[0])
    lis=time_2[0].split()
    if'くもり'in lis:
        if"晴れ"in lis:
                st.image(f'./image/{png[3]}',width= 200 )
        elif"雨"in lis:
                st.image(f'./image/{png[7]}',width= 200 )
        elif'くもり'in lis:
                st.image(f'./image/{png[4]}',width= 200 ) 
    elif'晴れ'in lis:
            st.image(f'./image/{png[9]}',width= 200 )
    elif'雨'in lis:
            st.image(f'./image/{png[8]}',width= 200 )
    elif'雪'in lis :
            st.image(f'./image/{png[6]}',width= 200 )
    elif'雷'in lis:
            st.image(f'./image/{png[2]}',width= 200 )
     

    with st.popover("降水確率"):
        for i in range(len(threedays_date2)):
            if days_date[0] in threedays_date2[i]:
                st.write(f"{threedays_date2[i]} {pops[i]}%")
        st.write(f"{threedays_date2[0]} {pops[0]}%")
    st.error("最高気温")
    st.write(f"{jma_temps2}℃")                                              
    st.info("最低気温")
    st.write(f"{jma_temps}℃")
with col2:
    st.header(threedays_date[1])
    st.write(time_2[1])
    lis=time_2[1].split()   
    if'くもり'in lis:
        if"晴れ"in lis:
                st.image(f'./image/{png[3]}',width= 200 )
        elif"雨"in lis:
                st.image(f'./image/{png[7]}',width= 200 )
        elif'くもり'in lis:
                st.image(f'./image/{png[4]}',width= 200 ) 
    elif'晴れ'in lis:
            st.image(f'./image/{png[9]}',width= 200 )
    elif'雨'in lis:
            st.image(f'./image/{png[8]}',width= 200 )
    elif'雪'in lis :
            st.image(f'./image/{png[6]}',width= 200 )
    elif'雷'in lis:
            st.image(f'./image/{png[2]}',width= 200 )
    with st.popover("降水確率"):
        for i in range(len(threedays_date2)):
            if days_date[1] in threedays_date2[i]:
                st.write(f"{threedays_date2[i]} {pops[i]}%")
    st.error("最高気温")
    st.write(f"{jma_temps2_2}℃")
    st.info("最低気温")
    st.write(f"{jma_temps_1}℃")
with col3:
    if length == 3:
        st.header(threedays_date[2])
        st.write(time_2[2])
        lis=time_2[2]
        if'くもり'in lis:
                if"晴れ"in lis:
                        st.image(f'./image/{png[3]}',width= 200 )
                elif"雨"in lis:
                        st.image(f'./image/{png[7]}',width= 200 )
                elif'くもり'in lis:
                        st.image(f'./image/{png[4]}',width= 200 ) 
                elif'雷'in lis:
                        st.image(f'./image/{png[1]}',width= 200 )
        elif'晴れ'in lis:
                st.image(f'./image/{png[9]}',width= 200 )
        elif'雨'in lis:
                st.image(f'./image/{png[8]}',width= 200 )
        elif'雪'in lis :
                st.image(f'./image/{png[6]}',width= 200 )
        elif'雷'in lis:
                st.image(f'./image/{png[2]}',width= 200 )
        with st.popover("降水確率"):
                st.write("ナニモナイヨ!")
        st.error("最高気温")
        st.write(f"{jma_temps2_4}℃")
        st.info("最低気温")
        st.write(f"{jma_temps_3}℃")

#まとめの説明書
#降水確率の24時間耐用
#飾り付けなど

col1a,col2a=st.columns(2)
with col1a:
    if st.button("雪"):
        st.snow()
with col2a:
    st.image('./image/雪.png', # 表示する画像の指定
          width= 100, # 画像の横幅(縦幅はアスペクト比に合わせて自動調整)
        )

