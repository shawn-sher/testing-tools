"""Tool for using urls"""
from os.path import dirname, realpath
import yaml
import requests
from requests.auth import HTTPBasicAuth

AGENT_HEADER = ('Mozilla/5.0 (X11; Linux x86_64; rv:31.0) '
                'Gecko/20100101 Firefox/31.0 Iceweasel/31.8.0')
ACCEPT_HEADER = ('text/html,application/xhtml+xml,'
                 'application/xml;q=0.9,*/*;q=0.8')
ACCEPT_LANGUAGE_HEADER = 'en-US,en;q=0.5'
ACCEPT_ENCODING_HEADER = 'gzip, deflate'
CONNECTION_HEADER = 'keep-alive'
INFO_YAML_PATH = realpath(dirname(__file__) + '/../info.yaml')


class TestUrl(object):
    """Class for testing a url"""
    def __init__(self, info_key, no_proxy=False):
        self.get_info(info_key)
        self.init_proxies(no_proxy)
        self.url = self.info['url']
        self.cookies = self.info.get('cookies', None)
        self.referer = self.info.get('referer', None)
        self.init_auth()
        self.init_headers()

    def get_info(self, info_key):
        """"Read info from yaml file"""
        passwd_dict = yaml.load(open(INFO_YAML_PATH).read())
        self.info = passwd_dict[info_key]

    def init_proxies(self, no_proxy):
        """Setup proxies unless no_proxy is set"""
        if no_proxy:
            self.proxies = None
        else:
            self.proxies = self.info.get('proxies', None)

    def init_auth(self):
        """init basic auth object"""
        user = self.info['user']
        passwd = self.info['passwd']
        self.auth = HTTPBasicAuth(user, passwd)

    def init_headers(self):
        """Set headers"""
        self.headers = {'User-Agent': AGENT_HEADER,
                        'Accept': ACCEPT_HEADER,
                        'Accept-Language': ACCEPT_LANGUAGE_HEADER,
                        'Accept-Encoding': ACCEPT_ENCODING_HEADER,
                        'Connection': CONNECTION_HEADER}
        if self.referer:
            self.headers['Referer'] = self.referer

    def get(self, params):
        """Perform a get request"""
        result = requests.get(self.url, auth=self.auth,
                              cookies=self.cookies, headers=self.headers,
                              proxies=self.proxies, params=params)
        return result

    def post(self, data, params=None, cookies=None, add_cookie_info=None):
        """Perform a post request"""
        if params is None:
            params = {}
        if cookies is not None:
            self.cookies = cookies
        if add_cookie_info is not None:
            self.cookies.update(add_cookie_info)

        result = requests.post(self.url, auth=self.auth, cookies=self.cookies,
                               headers=self.headers, proxies=self.proxies,
                               params=params, data=data)
        return result
