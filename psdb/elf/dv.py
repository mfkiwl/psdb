# Copyright (c) 2020 Phase Advanced Sensor Systems, Inc.


def dv_overlaps_region(dv, addr, size):
    '''
    Checks if any alp in the data vector overlaps the region defined by
    addr and size.
    '''
    for alp in dv:
        if addr < alp[0] + len(alp[1]) and addr + size > alp[0]:
            return True
    return False


assert (not dv_overlaps_region([(5, b'12345')],  0, 2))
assert (not dv_overlaps_region([(5, b'12345')],  1, 2))
assert (not dv_overlaps_region([(5, b'12345')],  2, 2))
assert (not dv_overlaps_region([(5, b'12345')],  3, 2))
assert (    dv_overlaps_region([(5, b'12345')],  4, 2))
assert (    dv_overlaps_region([(5, b'12345')],  5, 2))
assert (    dv_overlaps_region([(5, b'12345')],  6, 2))
assert (    dv_overlaps_region([(5, b'12345')],  7, 2))
assert (    dv_overlaps_region([(5, b'12345')],  8, 2))
assert (    dv_overlaps_region([(5, b'12345')],  9, 2))
assert (not dv_overlaps_region([(5, b'12345')], 10, 2))
assert (not dv_overlaps_region([(5, b'12345')], 11, 2))


def merge_dvs(lhs, rhs):
    '''
    Merges lhs and rhs, checking for address conflicts.  Alps from
    rhs will all follow vectors from lhs in the resulting merged vector.
    '''
    dv = lhs[:]
    for alp in rhs:
        if dv_overlaps_region(dv, alp[0], len(alp[1])):
            raise Exception('ALP(0x%08X, %u) overlaps!' % (alp[0], len(alp[1])))
        dv.append(alp)
    return dv
