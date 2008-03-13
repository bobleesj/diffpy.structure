#!/usr/bin/env python
"""Make a spheroid nanoparticle from a template structure."""

__id__ = "$Id$"

from diffpy.Structure import Structure, Atom
from numpy import array
from math import ceil

def makeEllipsoid(S, a, b=None, c=None):
    """Cut a structure out of another one.

    Arguments
    S       --  A Structure instance
    a       --  primary equatorial radius (along x-axis)
    b       --  secondary equatorial radius (along y-axis). If b is None
                (default) then it is set equal to a
    c       --  polar radius (along z-axis). If c is None (default), then it is
                set equal to a.

    Returns a new structure instance
    """
    if b is None: b = a
    if c is None: c = a
    sabc = array([a, b, c])

    # Create a supercell large enough for the ellipsoid
    frac = S.lattice.fractional(sabc)
    mno = map(ceil, 2*frac)
    # Make the supercell
    from supercell import supercell
    newS = supercell(S, mno)
    lat = newS.lattice

    # Find the central atom
    ncenter = findCenter(newS)

    cxyz = lat.cartesian(newS[ncenter].xyz)
    abc = array(newS.lattice.base.diagonal())

    delList = []
    N = len(newS)
    j = N
    for i in xrange(N):
        j -= 1

        # Calculate (x/a)**2 + (y/b)**2 + (z/c)**2
        xyz = lat.cartesian(newS[j].xyz)
        darray = ((xyz-cxyz)/sabc)**2
        d = sum(darray)**0.5

        # Discard atom if (x/a)**2 + (y/b)**2 + (z/c)**2 > 1
        if d > 1:
            delList.append(j)

    for i in delList:
        newS.pop(i)

    return newS

def findCenter(S):
    """Find the approximate center atom of a structure.

    The center of the structure is the atom closest to (0.5, 0.5, 0.5)

    Returns the index of the atom.
    """
    best = -1
    bestd = len(S)
    center = [0.5, 0.5, 0.5] # the cannonical center

    for i in range(len(S)):
        d = S.lattice.dist(S[i].xyz, center)
        if d < bestd:
            bestd = d
            best = i

    return best

if __name__ == "__main__":

    import os.path
    datadir = "../../tests/testdata"
    S = Structure()
    S.read(os.path.join(datadir, "CdSe_bulk.stru"), "pdffit")
    newS = makeEllipsoid(S, 20)
    newS.write("CdSe_d20.stru", "pdffit")
    newS = makeEllipsoid(S, 20, 10, 10)
    newS.write("CdSe_a20_b10_c10.stru", "pdffit")
    newS = makeEllipsoid(S, 20, 15, 10)
    newS.write("CdSe_a20_b15_c10.stru", "pdffit")
    S = Structure()
    S.read(os.path.join(datadir, "Ni.stru"), "pdffit")
    newS = makeEllipsoid(S, 20)
    newS.write("Ni_d20.stru", "pdffit")
    newS = makeEllipsoid(S, 20, 4)
    newS.write("Ni_a20_b4_c20.stru", "pdffit")
    newS = makeEllipsoid(S, 20, 15, 10)
    newS.write("Ni_a20_b15_c10.stru", "pdffit")

