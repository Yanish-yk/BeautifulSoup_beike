import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import re

def one_page_code(user_in_city):
 engine = create_engine('mysql+pymysql://root:passw0rd@localhost:3306/bieke')
 url = 'http://' + user_in_city + '.ke.com/ershoufang/jinjiang/pg{}/'
 for a in range(1, 100):
    url1 = url.format(a)
    header = {'User-Agent': '*********'}
    page = requests.get(url1, headers=header)
    a=page.text
    soup = BeautifulSoup(a,"lxml")
    #t_list=soup.find_all(class_="clear")
    list_1=soup.find_all(class_='title')
    home_name = []
    home_xiaoqu=[]
    home_info=[]
    home_followInfo=[]
    home_subway=[]
    home_totalprice=[]
    home_unitPrice=[]
    for i  in list_1 :
        home_name.append((i.get_text()).replace('\n', ''))    #拿房子名称
    home_name.remove('下载贝壳找房APP')
    list_xiaoqu=soup.find_all('div',class_='address')
    for soup_name_xiaoqu in list_xiaoqu:
        home_xiaoqu.append((soup_name_xiaoqu.find('a')).text)  #拿小区名称
    for soup_house_info in list_xiaoqu:
        home_info.append((soup_house_info.find('div','houseInfo')).text)                                     #拿房子具体信息
    for soup_followInfo in list_xiaoqu:
        str_temp=soup_followInfo.find('div','followInfo').text
        str_temp=str_temp.strip()
        str_temp=str_temp[0:4]
        str_temp=re.sub("\D","",str_temp)
        home_followInfo.append(str_temp) #关注信息
    for soup_subway in list_xiaoqu:
        if(None==(soup_subway.find('span','subway'))):
            home_subway.append(None)
        else:
            home_subway.append(soup_subway.find('span','subway').text)    #抓取是否近地铁
    for soup_totalprice in list_xiaoqu:
        tots=soup_totalprice.find('div','totalPrice').text
        tots=tots.replace('万','')
        home_totalprice.append(tots) #抓取价格

    for soup_unitPrice in list_xiaoqu :
        unitPrice=((soup_unitPrice.find('div', 'unitPrice')).text).replace('\n', '')

        temp_unit=(re.findall(r"\d+\.?\d*", unitPrice))
        temp_unit=str(temp_unit)
        temp_unit=temp_unit.replace('[\'','')
        temp_unit=temp_unit.replace('\']','')
        home_unitPrice.append(str(temp_unit))  # 抓取单价
    print("正在写入" + str(a) + "页数据")
    df_write=pd.DataFrame({'home_name':home_name,'home_xiaoqu':home_xiaoqu,'home_info':home_info,'home_followInfo':home_followInfo,'home_subway':home_subway,'home_totalprice':home_totalprice,'home_unitPrice':home_unitPrice})
    df_write.to_sql('bk_info', engine, if_exists='append',index=False)
    print("爬取" + str(a) + "页数据已完成!")
def main():
    # user_in_city = input('输入爬取城市：')
    one_page_code("cd")

if __name__ == '__main__':
    main()