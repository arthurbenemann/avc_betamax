import time
 
def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%30r %2.2f msec' % \
              (method.__name__, (te-ts)*1000)
        return result

    return timed