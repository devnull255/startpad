"""
Simple twitter API wrapper for python

Usage:

    twitter = Twitter()

    twitter.set_user_pass(user, passwd) - Set the user password for authenticated requests
    twitter.friends_ids(user) - pass username or id to get list of all friend ids
    twitter.update(text) - send an update for the current user ("tweet")
    twitter.calls_remaining - # of remaining apis that can be made this hour
    
ToDo:
    - Use shelf to cache results, especialy info about users and statuses.
    - Lightweight wrapper objects for User, Tweet/Status, List
        mckoss.tweets
        mckoss.timeline - iterator - goes all the way back in time!
        me.tweets
        me.timeline[3]
        mckoss.id
        mckoss.verified        
        
    - Global names for cached users ('mckoss', 'me', etc...)
    - abbreviated output formats for users and tweets
    - implement last[] for results of prior command(s)
"""

import simplejson
import urllib2
import urllib
import code
import sys
import re
import getpass
import shelve

# Just use this for error code description strings!
from BaseHTTPServer import BaseHTTPRequestHandler

sTwitter = "http://twitter.com/"
local_cache = "twitter_cache.bin"

TRACE = False

class Twitter(object):
    calls_remaining = 150
    opener = urllib2.build_opener()
    sUser = None
    
    def friends_ids(self, sUser=None):
        """
        Retrieves all the user ids of ones friends
        
        Note that if sUser is a numeric id, this api requires authentication
        """
        sUser = self.default_user(sUser)
        return self.api('friends/ids', self._screen_or_id(sUser))
        
    def users_show(self, sUser=None):
        sUser = self.default_user(sUser)
        return self.api('users/show', self._screen_or_id(sUser))

    def rate_limit_status(self):
        json = self.api('account/rate_limit_status')
        self.calls_remaining = json.remaining_hits
        return json
    
    def update(self, sText):
        return self.api('statuses/update', {'status':sText}, post=True)
    
    def get_lists(self, sUser=None):
        sUser = self.default_user(sUser)
        return self.api('1/%s/lists' % sUser)
    
    def get_list_members(self, list_id, sUser=None):
        sUser = self.default_user(sUser)
        return self.api('1/%s/%s/members' % (sUser, list_id))
    
    def post_list_members(self, list_id, new_user):
        sUser = self.default_user(None)
        return self.api('1/%s/%s/members' % (sUser, list_id), data={'id':new_user}, post=True)
    
    def friends_timeline(self):
        sUser = self.default_user(None)
        return self.api('statuses/friends_timeline')
    
    def default_user(self, sUser=None):
        if sUser == None:
            sUser = self.sUser
        if sUser is None:
            raise Exception("User not specified")
        return sUser
    
    @staticmethod    
    def _screen_or_id(sUser):
        sUser = str(sUser).strip()
        try:
            id = int(sUser)
            return {'user_id': id}
        except:
            return {'screen_name': sUser}
        
    def api(self, url, data=None, post=False):
        url = sTwitter + url + '.json'
        
        if not post and data is not None:
            url += '?' + urllib.urlencode(data)
            data = None
            
        if TRACE:
            print "url: %s" % url

        # Convert dictionary to URL encoded string
        try:
            if (data is not None):
                data = urllib.urlencode(data)
                if TRACE:
                    print "post: %s" % data
        
            sock = self.opener.open(url, data=data)
            headers = {}
            headers.update(sock.info().items())
            if 'x-ratelimit-remaining' in headers:
                self.calls_remaining = int(headers['x-ratelimit-remaining'])
            sJSON = sock.read()
            sock.close()
            json = simplejson.loads(sJSON)
        except urllib2.HTTPError, e:
            if TRACE:
                print "HTTPError %r" % e
            t2 = BaseHTTPRequestHandler.responses.get(e.code, ("unknown", "unknown"))
            json = {'error': "HTTP Error: %s (%s)" % (e.code, t2[0])}
        except Exception, e:
            json = {'error': "%r" % e}
        return MapWrapper(json)
    
    def set_user_pass(self, user, passwd):
        """
        Set a username and password for all subsequent calls to the twitter api.
        
        This is using Basic Authentication.
        """
        self.sUser = user

        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='Twitter API',
                                  uri='http://twitter.com',
                                  user=user,
                                  passwd=passwd)
        self.opener = urllib2.build_opener(auth_handler)
        
    def prompt_for_password(self):
        user = raw_input("Username: ").strip()
        if user == "":
            return
        passwd = getpass.getpass().strip()
        self.set_user_pass(user, passwd)
        


class TwitterCached(Twitter):
    sCache = "twitter_cache.bin"

    def __init__(self, sCache=None):
        super(TwitterCached, self).__init__()

        if sCache is not None:
            self.sCache = sCache
        self.mCache = shelve.open(self.sCache)

    def close(self):
        self.mCache.close()
        
class MapWrapper(object):
    """
    Wrap a mapping object, and return an object where the keys
    of the object can be accessed via attribute notation (much as in
    javascript: d.prop rather than d['prop'].
    
    We also make the json format be the repr for these objects.
    """
    _m = None
    _m_wrappers = {}
    
    def __new__(cls, m):
        """
        Share instances of MapWrapper for a given identify of map
        """
        if id(m) in cls._m_wrappers:
            return cls._m_wrappers[id(m)]
        mp = super(MapWrapper, cls).__new__(cls)
        cls._m_wrappers[id(m)] = mp
        mp._m = m
        return mp

    def __getattr__(self, name):
        value = self._m[name]
        if type(value) == dict:
            value = MapWrapper(value)
        return value
    
    def __setattr__(self, name, value):
        # We must initialize ._m as our first act!
        if self._m is None:
            super(MapWrapper, self).__setattr__(name, value)
            return
        
        if value is None:
            del self._m[name]
            return

        self._m[name] = value
        
    def __repr__(self):
        return simplejson.dumps(self._m, indent=4)
    
class TwitterUser(MapWrapper):
    pass
        
def test_me():
    tw = Twitter()

    fr = tw.friends_ids('mckoss')
    print "Found %d friends." % len(fr)
    
    assert(tw.calls_remaining == tw.rate_limit_status())
    
    fr = tw.friends_ids(1115651)
    print "Found %d friends." % len(fr)
    
    tw.prompt_for_password()

    try:
        tw.update('test - fail');
    except:
        print "Failed (expected)"
    
    tw.update('test - ignore')
    
rePrefix = re.compile(r"^[ \t]*", re.M)
def trim_prefix(s):
    return rePrefix.sub('', s)

def interactive():
    tw = Twitter()

    commands = ['update',
                'users_show',
                'friends_ids',
                'rate_limit_status',
                'api',
                'get_lists',
                'get_list_members',
                'post_list_members',
                'friends_timeline',
                ]

    class KeyWordCommands(object):
        """
        Present the set of available commands as a map - each of which
        calls a function to retrieve the value.
        """
        

    class TwitterHelp(object):
        s = """
        Twitter Interactive Interpreter Commands:
        -----------------------------------------
        login - prompt for a username and password
        
        update("tweet text")
        friends_ids([user])
        users_show([user])
        
        get_lists([user])
        get_list_members(list_name, [user])
        post_list_members(list_name, user_id)
        add_users_to_list(file_name, list_name)
        
        rate_limit_status() - query for current api call rate limit
        
        api(url, data) - other twitter api calls
        
        Example:
        
        my_friends = [users_show(x) for x in friends_ids()]
        -- returns array of all current users friends 
        
        exit/bye/quit - quit
        
        help - print this message
        """
        def __repr__(self):
           return trim_prefix(self.s.strip())
        
    class LoginCmd(object):
        def __repr__(self):
            tw.prompt_for_password()
            return ""
        
    class ExitCmd(object):
        def __repr__(self):
            sys.exit()
            return ""
            
    sys_display = sys.displayhook
    
    def json_display(value):
        # Hack to keep login from being double evaluated
        if type(value) == LoginCmd:
            sys_display(value)
            return
        try:
            s = simplejson.dumps(value, indent=4)
            print s
            print "API Calls remaining: %d" % tw.calls_remaining
        except:
            sys_display(value)
            
    def add_users_to_list(file_name, list_name):
        file = open(file_name)
        for user in file:
            user = user.strip()
            tw.post_list_members(list_name, user)
        file.close()

    d = {'help':TwitterHelp(),
         'login':LoginCmd(),
         'exit':ExitCmd(),
         'bye':ExitCmd(),
         'quit':ExitCmd(),
         'MapWrapper': MapWrapper}
    
    print TwitterHelp()
    for cmd in commands:
        d[cmd] = getattr(tw, cmd)
    d['add_users_to_list'] = add_users_to_list

    sys.displayhook = json_display
    
    code.interact("", local=d)
    
    tw.close()
    
if __name__ == '__main__':
    interactive()
