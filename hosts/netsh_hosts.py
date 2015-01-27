import requests

class NetshHostsCrawler(object):
    def __init__(self, opts):
        self.method_get = requests.get
        self.url = 'http://serve.netsh.org/pub/hosts.php'
        self.params = {
            'passcode': '16675',
            'validate': '34b8c',
            'gs': 'on',
            'wk': 'on',
            'twttr': 'on',
            'fb': 'on',
            'flkr': 'on',
            'dpbx': 'on',
            'odrv': 'on',
            'yt': 'on',
            'nolh': 'on'
        }
        opts = opts or {}
        for attr in opts:
            self.params[attr] = opts[attr] if opts[attr] else self.params[attr]
        self.timeout = 30000
        self.cookies = {
            'hostspasscode': '16675',
        }
        self.req = None
        self.hosts_content = None

    def crawl(self):
        self.req = self.method_get(url=self.url, \
            params=self.params, \
            cookies=self.cookies,\
            timeout=self.timeout)
        self.hosts_content = self.req.text

    def hosts(self):
        self.crawl()
        return self.hosts_content if self.hosts_content else ''

    def save(self, path='hosts.new'):
        import hashlib, datetime
        today_str = str(datetime.date.today())
        filehash = hashlib.new('md5', today_str).hexdigest()[:8] # hash length 8
        filename = path + filehash
        hosts = open(filename, 'w')
        hosts.write(self.hosts())
        print 'new hosts saved: %s' % filename


################### test ##################
# if __name__ == '__main__':
#     netsh = NetshHostsCrawler({
#         'gs': 'off',
#         'wk': 'off',
#     })
#     netsh.save()
################### test ##################
