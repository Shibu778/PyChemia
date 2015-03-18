"""
Mathematical operations
"""

__author__ = 'Guillermo Avendano-Franco'

import math
import numpy as _np
import itertools as _it
from fractions import gcd


def length_vector(v):
    """
    Returns the length of a vector 'v'
    Arbitrary number of dimensions

    :param v: list, numpy.ndarray
    :rtype : float

    Examples

>>> length_vector([1, 2, 3])
3.7416573867739413
    """
    return _np.linalg.norm(v)


def length_vectors(m):
    """
    Returns the lengths of several vectors
    arranged as rows in a MxN matrix

    :param m: numpy.ndarray

    :rtype : numpy.ndarray

    Examples

>>> length_vectors([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 0, 0], [0, 0, 2]])
array([  3.74165739,   8.77496439,  13.92838828,   1.        ,   2.        ])
    """
    m = _np.array(m)
    return _np.apply_along_axis(_np.linalg.norm, 1, m)


def unit_vector(v):
    """
    Returns the unit vector of the vector.
    Arbitrary number of dimensions

    :param v: list, numpy.array
    :rtype : numpy.ndarray

    Examples

>>> a = unit_vector([1, 2, 3])
>>> a
    array([ 0.26726124,  0.53452248,  0.80178373])
>>> length_vector(a)
    1.0
    """
    if length_vector(_np.array(v, dtype=float)) < 1E-10:
        raise ValueError('Vector is null')
    return _np.array(v) / length_vector(_np.array(v, dtype=float))


def unit_vectors(m):
    """
    Returns the unit vectors of a set
    of vectors arranged as rows in MxN matrix

    :param m: numpy.ndarray
    :rtype : numpy.ndarray

    Example:
>>> b = unit_vectors([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 0, 0], [0, 0, 2]])
>>> b
array([[ 0.26726124,  0.53452248,  0.80178373],
       [ 0.45584231,  0.56980288,  0.68376346],
       [ 0.50257071,  0.57436653,  0.64616234],
       [ 1.        ,  0.        ,  0.        ],
       [ 0.        ,  0.        ,  1.        ]])
>>> length_vectors(b)
array([ 1.,  1.,  1.,  1.,  1.])
    """
    return _np.divide(_np.array(m, dtype=float).T, length_vectors(_np.array(m, dtype=float))).T


def angle_vector(v1, v2, units='rad'):
    """
    Returns the angle in radians (default) or degrees
    between vectors 'v1' and 'v2'::

    :param v1: (list, numpy.ndarray)
    :param v2: (list, numpy.ndarray)
    :param units: (str) : 'rad' (default) Radians
                          'deg' Degrees
    :rtype : float

    Examples:
>>> angle_vector([1, 0, 0], [0, 1, 0])
1.5707963267948966
>>> angle_vector([1, 0, 0], [1, 0, 0])
0.0
>>> angle_vector([1, 0, 0], [-1, 0, 0])
3.1415926535897931
>>> angle_vector([1, 0, 0], [0, 1, 0], units='deg')
90.0
>>> angle_vector([1, 0, 0], [-1, 0, 0], units='deg')
180.0
    """
    assert (units in ['rad', 'deg'])

    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = _np.arccos(_np.dot(v1_u, v2_u))
    if _np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return _np.pi
    if units == 'rad':
        return angle
    elif units == 'deg':
        return 180.0 * angle / _np.pi


def angle_vectors(m, units='rad'):
    """
    Returns all the angles for all the
    vectors arranged as rows in matrix 'm'

    :param m: (numpy.ndarray)
    :param units: (str) : 'rad' Radians
                          'deg' Degrees

    :rtype : numpy.ndarray
    Example:

>>> a = angle_vectors([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 0, 0], [0, 0, 2]])
>>> import pprint
>>> pprint.pprint(a)
    {(0, 1): 0.22572612855273419,
     (0, 2): 0.2858867976945072,
     (0, 3): 1.3002465638163236,
     (0, 4): 0.6405223126794245,
     (1, 2): 0.060160669141772885,
     (1, 3): 1.0974779950809703,
     (1, 4): 0.8178885561654512,
     (2, 3): 1.0442265974045177,
     (2, 4): 0.86825103780276369,
     (3, 4): 1.5707963267948966}
>>> a = angle_vectors([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 0, 0], [0, 0, 2]], units='deg')
>>> pprint.pprint(a)
    {(0, 1): 12.933154491899135,
     (0, 2): 16.380106926405656,
     (0, 3): 74.498640433063002,
     (0, 4): 36.699225200489877,
     (1, 2): 3.4469524345065143,
     (1, 3): 62.880857226618922,
     (1, 4): 46.861562380328941,
     (2, 3): 59.829776886585428,
     (2, 4): 49.747120023952057,
     (3, 4): 90.0}
    """

    ret = {}
    for i in _it.combinations(range(len(m)), 2):
        ret[i] = angle_vector(m[i[0]], m[i[1]], units=units)
    return ret


def distance(v1, v2):
    """
    Return the vector v2-v1, the vector going from v1 to v2
    and the magnitude of that vector.

    :param v1: (list, numpy.ndarray)
    :param v2: (list, numpy.ndarray)
    :rtype : tuple

    Examples

>>> distance([0, 0, 0, 1], [1, 0, 0, 0])
(array([ 1,  0,  0, -1]), 1.4142135623730951)
>>> distance([-1, 0, 0], [1, 0, 0])
(array([2, 0, 0]), 2.0)
    """
    ret = _np.array(v2) - _np.array(v1)
    return ret, length_vector(ret)


def distances(m):
    """
    Return all the distances for all possible combinations
    of the row vectors in matrix m

    :param m: (list, numpy.ndarray)
    :rtype : dict

    Example:

>>> import pprint
>>> pprint.pprint(distances([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 0, 0], [0, 0, 2]]))
    {(0, 1): (array([3, 3, 3]), 5.196152422706632),
     (0, 2): (array([6, 6, 6]), 10.392304845413264),
     (0, 3): (array([ 0, -2, -3]), 3.6055512754639891),
     (0, 4): (array([-1, -2, -1]), 2.4494897427831779),
     (1, 2): (array([3, 3, 3]), 5.196152422706632),
     (1, 3): (array([-3, -5, -6]), 8.3666002653407556),
     (1, 4): (array([-4, -5, -4]), 7.5498344352707498),
     (2, 3): (array([-6, -8, -9]), 13.45362404707371),
     (2, 4): (array([-7, -8, -7]), 12.727922061357855),
     (3, 4): (array([-1,  0,  2]), 2.2360679774997898)}
    """
    ret = {}
    for i in _it.combinations(range(len(m)), 2):
        ret[i] = distance(m[i[0]], m[i[1]])
    return ret


def wrap2_pmhalf(x):
    """
    Wraps a number or array in the interval ]-1/2, 1/2]
    values = -1/2 will be wrapped  to 1/2

    :param x:

    Examples

>>> wrap2_pmhalf(-0.5)
0.5
>>> wrap2_pmhalf(0.0)
0.0
>>> wrap2_pmhalf([-0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75])
array([ 0.25,  0.5 , -0.25,  0.  ,  0.25,  0.5 , -0.25])
>>> wrap2_pmhalf([[-0.75, -0.5, -0.25], [0.25, 0.5, 0.75]])
array([[ 0.25,  0.5 , -0.25],
       [ 0.25,  0.5 , -0.25]])
    """

    def wrap(num):
        tol12 = 1e-12
        if num > 0:
            ret = (num + 0.5 - tol12) % 1.0 - 0.5 + tol12
        else:
            ret = -(-(num - 0.5 - tol12) % 1.0) + 0.5 + tol12
        for y in [-0.25, 0.0, 0.25, 0.5]:
            ret = (lambda num2: y if abs(y - num2) < tol12 else num2)(ret)
        return ret

    if _np.iterable(x):
        vec = _np.vectorize(wrap)
        return vec(x)
    else:
        return wrap(x)


def vector_set_perpendicular(vector3):
    """
    Produces a set of three mutually perpendicular vectors
    The two other vectors will be unitary

    :return: (tuple) Two numpy arrays
    """
    v1 = unit_vector(vector3)
    v2 = None
    v3 = None
    while True:
        other = unit_vector(_np.random.rand(3))
        if _np.abs(_np.dot(v1, other)) > 0.05:
            v2 = unit_vector(_np.cross(v1, other))
            v3 = unit_vector(_np.cross(v1, v2))
            break
        else:
            continue
    # print _np.dot(v1, v2)
    # print _np.dot(v1, v3)
    # print _np.dot(v2, v3)

    # assert (_np.abs(_np.dot(v1, v2)) < 1E-15)
    # assert (_np.abs(_np.dot(v1, v3)) < 1E-15)
    # assert (_np.abs(_np.dot(v2, v3)) < 1E-15)
    return v1, v2, v3


def matrix_from_eig(v1, v2, v3, lam1, lam2, lam3):
    """
    Given 3 eigenvectors and 3 eigenvalues, returns the
    matrix A that has those eigenvectors and eigenvalues.

    The matrix $A = P.D.P^{-1}$

    Where P is the column stack of eigenvectors and
    D is a diagonal matrix of eigevalues

    :param v1: First eigenvector
    :param v2: Second eigenvector
    :param v3: Third eigenvector
    :param lam1: First eigenvalue
    :param lam2: Second eigenvalue
    :param lam3: Third eigenvalue
    :return: (numpy.ndarray) The matrix
    """
    matrixp = _np.vstack((v1, v2, v3)).T
    matrixd = _np.diag([lam1, lam2, lam3])
    matrixpinv = _np.linalg.inv(matrixp)
    matrixa = _np.dot(matrixp, _np.dot(matrixd, matrixpinv))
    return matrixa


def integral_gaussian(a, b, mu, sigma):
    """
    Computes the integral of a gaussian centered
    in mu with a given sigma
    :param a:
    :param b:
    :param mu:
    :param sigma:
    :return:
    """

    # Integral from -\infty to a
    val_floor = 0.5 * (1 + math.erf((a - mu) / (sigma * math.sqrt(2.0))))

    # Integral from -\infty to b
    val_ceil = 0.5 * (1 + math.erf((b - mu) / (sigma * math.sqrt(2.0))))

    return val_ceil - val_floor


def frexp10(x):
    exp = int(math.floor(math.log10(abs(x))))
    return x / 10 ** exp, exp


def round_small(number, ndigits=0):
    mantissa, exponent = frexp10(number)
    mantissa = round(mantissa, ndigits)
    return mantissa * 10 ** exponent


def sieve_atkin(limit):
    ret = [2, 3]
    sieve = [False]*(limit+1)
    for x in range(1, int(math.sqrt(limit))+1):
        for y in range(1, int(math.sqrt(limit))+1):
            n = 4*x*x + y*y
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                sieve[n] = not sieve[n]
            n = 3*x*x+y*y
            if n <= limit and n % 12 == 7:
                sieve[n] = not sieve[n]
            n = 3*x*x - y*y
            if x > y and n <= limit and n % 12 == 11:
                sieve[n] = not sieve[n]
    for x in range(5, int(math.sqrt(limit))):
        if sieve[x]:
            for y in range(x*x, limit+1, x*x):
                sieve[y] = False
    for p in range(5, limit):
        if sieve[p]:
            ret.append(p)
    return ret


def trial_division(n):
    """
    Return a list of the prime factors for a natural number
    uses the Sieve of Atkin as a list of primes

    :param n: (int) A natural number

    :rtype : (list)
    """
    if n == 1:
        return [1]
    primes = sieve_atkin(int(n**0.5) + 1)
    prime_factors = []

    for p in primes:
        if p*p > n:
            break
        while n % p == 0:
            prime_factors.append(p)
            n /= p
    if n > 1:
        prime_factors.append(n)

    return prime_factors


def lcm(a, b):
    """
    Return the Least Common Multiple
    the smallest positive integer that is divisible by both a and b
    :param a: (int)
    :param b: (int)
    :return: (int)

    :rtype : (int)
    """
    return a*b/gcd(a, b)


def shortest_triple_set(n):
    """
    Return the smallest three numbers (a,b,c) such as
    a*b*c=n
    And a+b+c is as small as possible

    :param n:
    :return:
    """
    # First Compute the prime factors
    prime_factors = trial_division(n)

    if len(prime_factors) == 3:
        # No choice return the three numbers
        return prime_factors
    elif len(prime_factors) < 3:
        # If there are less than 3 complete the set with ones
        while len(prime_factors) % 3 != 0:
            prime_factors = [1]+prime_factors
        return prime_factors
    else:
        factors = _np.array(prime_factors)
        while len(factors) > 3:
            print factors
            # Complete a multiple of 6 and sum folding lowest with highest
            while len(factors) % 6 != 0:
                factors = _np.concatenate(([1], factors))
            # Take the first half
            low = factors[:len(factors)/2]
            # take the second half and invert the order
            high = factors[len(factors)/2:][::-1]
            # Sum both arrays and sort them before reenter
            factors = _np.sort(low * high)
        return list(factors)


def rotation_matrix_axis_angle(axis, theta):
    # Given a unit vector u = (ux, uy, uz), where ux**2 + uy**2 + uz**2 = 1,
    u = unit_vector(axis)
    # with ux is the cross product matrix
    ux = _np.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]])
    # uxu is the tensor product of u
    uxu = _np.tensordot(u, u.T, axes=0)
    # This is a matrix form of Rodrigues 'rotation formula'
    return _np.cos(theta)*_np.identity(3) + _np.sin(theta)*ux + (1-_np.cos(theta))*uxu
