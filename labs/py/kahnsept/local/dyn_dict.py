import UserDict

class DynDict(UserDict.DictMixin):
    """
    Implement a dynamic dictionary object, which acts as the union of the dictionaries
    from which it was created.
    
    The first dictionary is searched first, and subsequent dictionaries are searched when no results are found.
    
    New elements are always created in the first dictionary.
    """
    
    def __init__(self, *args):
        self.dicts = args
        
    def __getitem__(self, key):
        for d in self.dicts:
            if key in d:
                return d[key]
        raise KeyError
        
    def __setitem__(self, key, value):
        self.dicts[0][key] = value
        
    def __delitem__(self, key):
        for d in self.dicts:
            if key in d:
                del d[key]
                
    def keys(self):
        s = set()
        for d in self.dicts:
            s.update(d.keys())
        return list(s)
        
    