# Copyright (c) 2019 Phase Advanced Sensor Systems, Inc.
import psdb
from .flash import FLASH
from ..device import MemDevice
from psdb.targets import Target


class STM32H7ROMTable1(psdb.component.Component):
    '''
    Matcher for the STM32H7 System ROM Table 1.  This ROM table is found on
    AP2 at address 0xE00E0000.  In order to probe child components on AP2, we
    need to enable the D1/D3/Trace clocks via DBGMCU_CR.
    '''
    def __init__(self, component, subtype):
        super(STM32H7ROMTable1, self).__init__(component.parent, component.ap,
                                               component.addr, subtype)
        self.write_dbgmcu_cr(0x00700000)

    def write_dbgmcu_cr(self, v):
        self.ap.write_32(v, 0xE00E1004)


class STM32H7(Target):
    def __init__(self, db):
        super(STM32H7, self).__init__(db)
        self.ahb_ap     = self.db.aps[0]
        self.apbd_ap    = self.db.aps[2]
        self.uuid       = self.ahb_ap.read_bulk(0x1FF1E800, 12)
        self.flash_size = (self.ahb_ap.read_32(0x1FF1E880) & 0x0000FFFF)*1024
        self.mcu_idcode = self.apbd_ap.read_32(0xE00E1000)
        self.flash      = FLASH(self, 'FLASH', 0x52002000, 0x08000000)
        MemDevice(self, 'FBANKS', self.flash.mem_base, self.flash.flash_size)

    def __repr__(self):
        return 'STM32H7xx MCU_IDCODE 0x%08X' % self.mcu_idcode

    @staticmethod
    def probe(db):
        # APSEL 0 and 2 should be populated.
        if 0 not in db.aps:
            return None
        if 2 not in db.aps:
            return None

        # APSEL 0 should be an AHB AP.
        ap = db.aps[0]
        if not isinstance(ap, psdb.access_port.AHBAP):
            return None

        # Identify the STM32H7 through the base component's CIDR/PIDR
        # registers.
        c = db.aps[0].base_component
        if not c or c.cidr != 0xB105100D or c.pidr != 0x00000000000A0450:
            return None

        # There should be exactly one CPU.
        if len(db.cpus) != 1:
            return None

        return STM32H7(db)


psdb.component.StaticMatcher(STM32H7ROMTable1, 2, 0xE00E0000,
                             0xB105100D, 0x00000000000A0450,
                             subtype='STM32H7 ROM Table 1')
