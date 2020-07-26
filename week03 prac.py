import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200726'
data = requests.get(url, headers=headers)
    # &hh=21&rtm=N&pg=  + str(page)
soup = BeautifulSoup(data.text, 'html.parser')

pages = soup.select('#body-content > div.page-nav.rank-page-nav > a')
maximum_page =0
for songs_page in pages : #마지막 page값을 구하는 반복문입니다.

    if songs_page is not None:
        maximum_page += 1
print("총" + str(maximum_page) + "개의 페이지가 확인 되었습니다.")

url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200726&hh=23&rtm=Y&pg='

for page_num in range(1, maximum_page+1):
    data = requests.get(url+str(page_num), headers=headers)
    # &hh=21&rtm=N&pg=  + str(page)
    soup = BeautifulSoup(data.text, 'html.parser')
    song_list = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

    for song in song_list:
        rank = song.select_one('td.number').contents[0].strip()
        title = song.select_one('td.info > a.title.ellipsis').text.strip()
        artist = song.select_one('td.info > a.artist.ellipsis').text.strip()

        icon_tag = song.select_one('span.icon')
        if icon_tag is not None:
            title = song.select_one('td.info > a.title.ellipsis').contents[1].text +')'
            icon_tag.decompose()
            title += song.select_one('td.info > a.title.ellipsis').text.strip()
        print(rank, title, artist)

        songs = {
            'rank': rank,
            'title': title,
            'artist': artist
        }

        db.songs_rank.insert_one(songs)


    #rank selector = #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
    #title selector = #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
    #artist selector = #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
    #pagination = #body-content > div.page-nav.rank-page-nav > a:nth-child(2)