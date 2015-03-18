"""
Routines related to Metadata info and Repositories
"""

try:
    import pymongo
    USE_MONGO = True
except ImportError:
    print 'Could no import pymongo, mongo database functionality disabled'
    USE_MONGO = False

if USE_MONGO:
    from _db import PyChemiaDB, get_database, object_id, create_user


# __all__ = filter(lambda s: not s.startswith('_'), dir())

