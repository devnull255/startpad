import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.1')

import sys
import logging
import google.appengine.ext.webapp.util
import django.core.handlers.wsgi
import django.conf

# Force Django to reload its settings.  TODO - really needed?
django.conf.settings._target = None

def log_exception(*args, **kwds):
    logging.exception('Exception in request:')

def real_main():
    # Create a Django application for WSGI.
    application = django.core.handlers.wsgi.WSGIHandler()
    google.appengine.ext.webapp.util.run_wsgi_app(application)
    
def profile_main():
    # This is the main function for profiling 
    # We've renamed our original main() above to real_main()
    import cProfile, pstats, StringIO
    prof = cProfile.Profile()
    prof = prof.runctx("real_main()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("cumulative")  # time or cumulative
    stats.print_stats(80)  # lines to print
    # The rest is optional.
    # stats.print_callees()
    # stats.print_callers()
    logging.info("Profile data:\n%s", stream.getvalue())

# Rename main to profile_main to enable profiling 
main = real_main
    
if __name__ == '__main__':
  main()
