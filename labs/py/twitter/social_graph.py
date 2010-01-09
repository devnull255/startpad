import twitter
import simplejson
import shelve

class GraphCollector():
    """
    Manage reading the social graph of a number of users and caching them
    locally. 
    """
    tw = twitter.Twitter()
    
    def __init__(self, sCollection):
        self.mCollection = shelve.open(sCollection)
        print "Initial users in database: %d" % len(self.mCollection)
        
    def collect(self, users):
        print "Collecting %d users" % len(users)
        
        for user in users:
            try:
                sName = str(user['name'])
    
                if sName in self.mCollection:
                    if len(self.mCollection[sName]['graph']) > 0:
                        #print "%s already in collection" % sName
                        continue
                    print "%s in collection BUT, has zero friends - try again" % sName
                
                if self.tw.calls_remaining < 50:
                    print "Only %d twitter API calls remaining this hour" % self.tw.calls_remaining
                    break
                
                print "Getting %s graph from twitter (%d calls remaining)" % (sName, self.tw.calls_remaining)
                ids = self.tw.friends_ids(sName)
                user['graph'] = ids
                self.mCollection[sName] = user
                self.mCollection.sync()
                print "Found %d friends for %s" % (len(ids), sName)
            except Exception, e:
                print "Error getting friends for %s (%r)" % (sName, e) 
            
    def get_user_ids(self):
        print "Updating (bogus search-based) user ids"

        i = 0
        
        for (name, user) in self.mCollection.items():
            if 'fixed' not in user:
                try:
                    i += 1
                    user_info = self.tw.users_show(name)
                    user['id'] = user_info['id']
                    assert(type(user['id']) == int)

                    # Ensure user gets written back!
                    user['fixed'] = True                    
                    self.mCollection[name] = user
                    self.mCollection.sync()

                    print "%d. Updated id for %s = %d (%d remaining)" %\
                            (i, name, user['id'], self.tw.calls_remaining)
                except:
                    print "--- error updating %s ---" % name

    def get_tweet_secs(self, users):
        for user in users:
            name = str(user['name'])
            if name not in self.mCollection:
                print "%s is not in the database - skipping" % name
                continue                

            try:
                userDB = self.mCollection[name]
            except:
                print "error reading: %s" % name
                continue

            userDB['tweet_secs'] = int(user['tweet_secs'])
            self.mCollection[name] = userDB
            print "Updated tweet_secs for %s" % name
            self.mCollection.sync()
                
    def close(self):
        print "Final number of users in database: %d" % len(self.mCollection)
        
        self.mCollection.close()
        self.mCollection = None

    def id_map(self):
        mID = {}
        for name in self.mCollection:
            try:
                user = self.mCollection[name]
                if type(user['id']) == int:
                    mID[user['id']] = user
            except:
                print "Can't read %s" % name
        return mID
        
    def dump_users(self):
        mID = self.id_map()

        self.graph = {}
        for name in self.mCollection:
            try:
                userDB = self.mCollection[name]
            except:
                print "can't read user %s" % name
                continue
            user = {}
            self.graph[name] = user

            user['name'] = name
            user['id'] = userDB['id']
            user['friend_count'] = len(userDB['graph'])
            user['tweet_id'] = userDB['tweet_id']
            user['tweet_secs'] = userDB['tweet_secs']
            user['all_children'] = set()

            if 'graph' not in userDB:
                continue

            parents = []
            for id in userDB['graph']:
                if id not in mID:
                    continue
                userOther = mID[id]
                # Add other user name if they tweeted first
                if user['tweet_id'] > userOther['tweet_id']:
                    parents.append(userOther['name'])

            if len(parents) == 0:
                parents = ['mckoss']
            user['parents'] = parents

        for (name, user) in self.graph.items():
            for parent in user['parents']:
                if 'children' not in self.graph[parent]:
                    self.graph[parent]['children'] = []
                self.graph[parent]['children'].append(name)

        self.shortest_path('mckoss', [])

        for user in self.graph.values():
            user['total_tweets'] = len(user['all_children'])
            del user['all_children']
                    
        sJSON = simplejson.dumps(self.graph, indent=4)
        print sJSON

    def shortest_path(self, name, path):
        user = self.graph[name]
        user['all_children'].add(name)
        
        if 'path' in user:
            if len(path) < len(user['path']):
                user['path'] = list(path)
            return
        else:
            user['path'] = list(path)

        if 'mckoss' in user['path'] and user['path'][0] != 'mckoss':
            print "Non-root path: %r" % user['path']

        if 'children' not in user:
            return

        path.append(name)
        for child in user['children']:
            self.shortest_path(child, path)
            childT = self.graph[child]
            user['all_children'].update(childT['all_children'])
        path.pop()
            
            
def grab_graph():
    """
    Use the graph collector to update the database from the users
    on the aids_day retweet challenge.
    """
    gc = GraphCollector("aids_day_graph.bin")
    gc.tw.prompt_for_password()
    file = open("aids_day_users.json")
    sUsers = file.read()
    users = simplejson.loads(sUsers)
    gc.collect(users)
    gc.get_user_ids()
    gc.close()
    
def update_tweet_secs():
    gc = GraphCollector("aids_day_graph.bin")
    file = open("aids_day_users.json")
    sUsers = file.read()
    users = simplejson.loads(sUsers)
    gc.get_tweet_secs(users)
    gc.close()

if __name__ == '__main__':
    gc = GraphCollector("aids_day_graph.bin")
    gc.dump_users()
    gc.close()
