import streamlit as st
import requests

def getAllBookstore():
	url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M'
	headers = {"accept": "application/json"}
	response = requests.get(url, headers=headers)
	return response.json()

def getCountyOption(items):
    optionList = []
    for item in items:
        city = item['cityName'][:3]
        if city not in optionList:
            optionList.append(city)
    return optionList

def getDistrictOption(items, target):
    optionList = []
    for item in items:
        name = item['cityName']
        if target not in name:
            continue
        name.strip()
        district = name[5:]
        if len(district) == 0:
            continue
        if district not in optionList:
            optionList.append(district)
    return optionList

def getSpecificBookstore(items, county, districts):
    specificBookstoreList = []
    for item in items:
        name = item['cityName']
        if county not in name:
            continue
        for district in districts:
            if district not in name:
                break
        else:
            if name not in specificBookstoreList:
                specificBookstoreList.append(item)
    return specificBookstoreList

def getBookstoreInfo(items):
    expanderList = []
    for item in items:
        expander = st.expander(item['name'])
        expander.image(item['representImage'])
        expander.metric('hitRate', item['hitRate'])
        expander.subheader('Introduction')
        expander.write(item['intro'])
        expander.subheader('Address')
        expander.write(item['address'])
        expander.subheader('Open Time')
        expander.write(item['openTime'])
        expander.subheader('Email')
        expander.write(item['email'])
        expanderList.append(expander)
    return expanderList

def app():
    st.header('特色書店地圖')
    st.metric('Total bookstore',len(getAllBookstore()))
    county = st.selectbox('請選擇縣市', getCountyOption(getAllBookstore())) 
    district = st.multiselect('請選擇區域', getDistrictOption(getAllBookstore(),county))
    bookstores_list = getSpecificBookstore(getAllBookstore(),county,district)
    st.write(f'總共有{len(bookstores_list)}項結果')
    bookstores_list.sort(key = lambda item: item['hitRate'], reverse=True)
    bookstoreInfo = getBookstoreInfo(bookstores_list)

if __name__ == '__main__':
    app()