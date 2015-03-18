"""
Routines related to symmetry identification and manipulation.
The routines and classes heavily rely on spglib
"""

# __all__ = filter(lambda s: not s.startswith('_'), dir())

try:
    import pyspglib._spglib as spg
    USE_SPGLIB = True
except ImportError:
    print 'SPGLIB not found, symmetry module disabled'
    USE_SPGLIB = False

if USE_SPGLIB:
    from _spglib import StructureSymmetry, symmetrize
