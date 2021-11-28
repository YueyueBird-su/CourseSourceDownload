from bs4 import BeautifulSoup
import requests
import getpass

print("注：输入的cookie不可见，不要使用Ctrl+C粘贴，这样只会粘贴第一个字符。\n！！！请点击鼠标右键进行粘贴！！！")
cookie=getpass.getpass("输入你的教务网网页登陆后的Cookie: ")
if len(cookie)==0:
    print("cookie输入失败，请重新输入！")
    input("输入任何键退出")
    exit()
else:
    print("cookie长度为：%d,正在尝试连接。"%len(cookie))

header={
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': cookie,
    'Referer': 'http://jwc.swjtu.edu.cn/vatuu/UserFramework',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'
}
Url="http://jwc.swjtu.edu.cn/vatuu/StudentTeachResourceAction?setAction=teachCourse"
Url_pre="http://jwc.swjtu.edu.cn/"

html=requests.get(Url,headers=header).text
soup=BeautifulSoup(html,'lxml')

links_a=soup.find_all('a')[2:]
num_d = 0
num_f = 0
for course in links_a:
    num=0
    courseName=course['href'].split('./')[-1].split('=')[-1]
    courseLink=course['href'].split('./')[-1]
    url=Url_pre+courseLink

    html2=requests.get(url,headers=header).text
    soup2=BeautifulSoup(html2,'lxml')
    links=soup2.find_all('a')[2:]
    if len(links)>0:
        print("正在下载《%s》课程资源"%courseName)
        import os
        os.makedirs('./FindCourse/' + courseName, exist_ok=True)
        for Link in links:
            # 资源下载页面的下载链接
            sourceLink=Link['href']
            sourceLink_p=sourceLink.split('teachResourceView')

            # 载入下载页面，获取资源名称
            showLink=Url_pre+sourceLink.split('./')[-1]
            html3=requests.get(showLink,headers=header).text
            soup3=BeautifulSoup(html3,'lxml')
            rows=[row.get_text() for row in soup3.find_all('td',style="color: #0EA33F")]
            fileName_p=rows[0]
            fileName=rows[0].split('.')[0]

            # 所有资源的下载链接
            fileLink=(sourceLink_p[0]+'downloadTeachResource'+sourceLink_p[1]).split('./')[-1]
            fileLink=Url_pre+fileLink

            # 资源请求
            try:
                # urllib.request.urlretrieve(fileLink,r'./FindCourse/' + courseName +'/' + fileName_p)
                r = requests.get(fileLink, stream=True)
                with open('./FindCourse/%s/%s' %(courseName,fileName_p), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=128):
                        f.write(chunk)
                num += 1
                num_d += 1
                length=int((num / len(links)) * 100)
                str='['+"="*length+" "*(100-length)+"] %d"%length+"%"
                print(str)

            except:
                num += 1
                num_f += 1
                length=int((num / len(links)) * 100)
                str='['+"="*length+" "*(100-length)+"] %d"%length+"%"
                print(str)

        print('-'*100)

print("所有学习资源下载已结束，累计成功 %d 个，失败 %d 个"%(num_d,num_f))

if num_d+num_f==0:
    print("下载失败，请重新获取cookie或再次尝试！")
    input("输入任何键退出")