import twitter
import simplejson as json
from datetime import datetime
import time

# One update per minute - to stay clear of twitter update limits (250/hour?)
wait = 90

def make_namelist():
    file = open('all_tweeters.js')
    d = json.load(file)
    for name in d:
        print name
    file.close()
    
    file = open('name_list.txt', 'w')
    for name in d:
        file.write(name + '\n')
    file.close()
    
def join_me(start_after=None):
    tw = twitter.Twitter()
    tw.prompt_for_password()

    file = open('name_list.txt')
    names = []
    for name in file.readlines():
        name = name.strip()
        if start_after is None:
            names.append(name)
            continue
        if name != start_after:
            continue
        start_after = None
    file.close()
    
    file_log = open('sent.log', 'a')
    file_log.write('Starting %s\n' % datetime.now())
    
    tweet = "@%s Thanks for re-tweeting my AIDS-DAY Challenge - now will you join me to double our impact? - http://www.Quip-Art.com/24Y"
    
    for name in names:
        try:
            print name
            
            res = tw.update(tweet % name)
            if hasattr(res, 'error'):
                raise Exception(res.error)
            file_log.write("%s: %s\n" % (name, res.id))
            time.sleep(wait)
        except Exception, e:
            print "%s: error (%r)\n" % (name, e)
            file_log.write("%s: error (%r)\n" % (name, e))
            
    file_log.close()
    
if __name__ == '__main__':
    join_me('CLEEVN')