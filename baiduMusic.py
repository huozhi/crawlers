# encoding=utf8  

from bs4 import BeautifulSoup
import requests

class MusicInfo(object):
    def __init__(self, title, singer, albumTitle):
        self.title = title
        self.singer = singer
        self.albumTitle = albumTitle

    def __str__(self):
        return str((self.title, self.singer, self.albumTitle))


class BaiduMusicCrawler(object):
    def __init__(self, songName):
        self.music = { }
        if songName: self.music["key"] = songName

    def crawl(self):
        result = []
        req = requests.get("http://music.baidu.com/search/song", params=self.music)
        soup = BeautifulSoup(req.text)
        musicList = soup.find("div", class_="song-list").find("ul").find_all("li")
        for musicInfo in musicList:
            songItem = musicInfo.find("div", class_="song-item")
            title = songItem.find("span", class_="song-title").get_text(strip=True)
            singer = songItem.find("span", class_="singer").get_text(strip=True)
            albumTitle = songItem.find("span", class_="album-title").get_text(strip=True)
            songInfo = MusicInfo(title, singer, albumTitle)
            result.append(songInfo)
        return result
    
########################################################
# if __name__ == '__main__':
#     crawler = BaiduMusicCrawler('play with boosty')
#     for each in crawler.crawl():
#         print each
########################################################
