# Copyright (c) 2018-2019 Phase Advanced Sensor Systems, Inc.
from . import cortex
from ..targets import scs_v6_m


class CortexM0P(cortex.Cortex):
    def __init__(self, component, subtype):
        super(CortexM0P, self).__init__(component, subtype)

    def make_scs(self, target):
        return scs_v6_m.SCS(self.scb.ap, 'SCS%u' % self.cpu_index,
                            self.scb.addr, target=target)
