import collections
import collections.abc
import inspect
 
if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable
 
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec
