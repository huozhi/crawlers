import requests
import json
import re
import datetime


# ?format=json&method=flickr.interestingness.getList&api_key=%s&date=%s'

class FlickrInterestness(object):
    url = 'https://api.flickr.com/services/rest/'

    def __init__(self, api_key):
        date = str(datetime.date.fromordinal(datetime.date.today().toordinal() - 1))
        self.params = {
            'format': 'json',
            'method': 'flickr.interestingness.getList',
            'api_key': api_key,
            'date': date
        }

    def crawl(self):
        res = requests.get(FlickrInterestness.url, params=self.params)
        jsonp = res.text
        apijson = re.sub(r'([a-zA-Z_0-9\.]*\()|(\);?$)','',jsonp)
        data = json.loads(apijson)
        phosts = data.get('photos').get('photo')

        # picurl = 'https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}_[mstzb].jpg'
        picurl_format = 'https://farm%d.staticflickr.com/%s/%s_%s_b.jpg'
        # picurl_format = 'https://www.flickr.com/photos/%s/%s/'

        picurls = []
        for photo in phosts:
            farm = photo.get('farm')
            server_id = photo.get('server')
            picture_id = photo.get('id')
            secret = photo.get('secret')
            owner = photo.get('owner')
            picurl = picurl_format % (farm, server_id, picture_id, secret)
            # picurl = picurl_format % (owner, picture_id)
            picurls.append(picurl)
        return picurls


# if __name__ == '__main__':
#     fi = FlickrInterestness('YOUR_FLICKR_API_KEY')
#     print fi.crawl()
