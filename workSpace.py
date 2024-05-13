import requests
from bs4 import BeautifulSoup # type: ignore
import pandas as pd # type: ignore


data = []
codePostal =  [1000,1020,1030,1040,1050,1060,1070,1080,1082,1130,1140,1150,1160,1170,1180,1190 ]
codePostal1 = [1200,1210,1300,1310,1348,1400,1410,1420,1600,1702,1780,1800,1804,1831,1853,1930 ]
codePostal2 = [1935,1950 ,1970,2000,2018,2030,2100,2140,2160,2170,2200,2300,2440,2500,2600,2630]
codePostal3 = [2660,2800,2830,2960,3000,3001,3500,3530,3580,3590,3600,3640,3800,3900,3920,4000 ]
codePostal4 = [4020,4557,5000,5100,5101,6900,7000,7110,7500,7503,7700,8000,8020,8200,8400,8500 ]
codePostal4 = [8530,8560,8790,8800,8870,9000,9050,9080,9100,9140,9300,9320,9506,9700,9820]


def searchByURL(url):

    res = requests.get(url,timeout= 10000 ) 
    pageContent = BeautifulSoup(res.content,"html.parser")
    liste_workspace = pageContent.find("ul",{"class":"list_workspaces list-inline"})
    contents = liste_workspace.find_all("div",{"class":"content"})

    for content in contents:
        contentData = {}
        rue = " ".join(content.find("p").text.split(" ")[:-2])


        postal = " ".join(content.find("p").text.split(" ")[-2:])[:-8]
        workSpace =content.find("h3").text
        c =""
        nb = postal.split(" ")[0]

        if len(nb) == 6:
            rue +=" "+nb[0:2]
            c = nb[2:]
        elif len(nb) == 7:
            rue += " "+nb[0:3]
            c = nb[3:]
        elif len(nb) == 11:
            rue += " "+nb[0:7]
            c = nb[7:]
        elif len(nb) == 5:
            rue += " "+nb[0:1]
            c = nb[1:]
        elif len(nb) == 10:
            rue += " "+nb[0:5]
            c = nb[5:]
        elif len(nb) == 9:
            rue += " "+nb[0:5]
            c = nb[5:]

            
        contentData["workSpace"] = workSpace
        contentData["Rue"] =rue
        contentData["Code Postal"] = c +" "+ postal.split(" ")[1]

        if content.find("p",{"class":"type"}):
            contentData["type"] = content.find("p",{"class":"type"}).text.strip()
        else:
            contentData["type"] = "None"
        data.append(contentData)



for code in codePostal:
    print(code)
    for page in range(1,100):
        url =  "https://belgianworkspaceassociation.be/centers/page/{}/?search&cp={}&type&startwith".format(page,code) 
        res = requests.get(url)
        pageContent = BeautifulSoup(res.content,"html.parser")
        liste_workspace = pageContent.find("ul",{"class":"list_workspaces list-inline"})

        if liste_workspace.li :
            searchByURL(url)
        else:
            break

dataFrame = pd.DataFrame(data)
dataFrame.to_csv('workspace.csv', index=False , encoding ="utf-8-sig")
#print(data)
