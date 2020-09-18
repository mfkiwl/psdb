# Copyright (c) 2019 Phase Advanced Sensor Systems, Inc.
import psdb
from .rom_table_1 import STM32H7ROMTable1
from psdb.devices import MemDevice, stm32h7
from psdb.targets import Target


DEVICES = [(stm32h7.FLASH_DP,   'FLASH',    0x52002000, 0x08000000, 3300000),
           ]


class STM32H7_DP(Target):
    def __init__(self, db):
        super(STM32H7_DP, self).__init__(db, 24000000)
        self.m7_ap      = self.db.aps[0]
        self.m4_ap      = self.db.aps[3]
        self.apbd_ap    = self.db.aps[2]
        self.ahb_ap     = self.m7_ap
        self.uuid       = self.ahb_ap.read_bulk(0x1FF1E800, 12)
        self.flash_size = (self.ahb_ap.read_32(0x1FF1E880) & 0x0000FFFF)*1024
        self.mcu_idcode = self.apbd_ap.read_32(0xE00E1000)

        for d in DEVICES:
            cls  = d[0]
            name = d[1]
            addr = d[2]
            args = d[3:]
            cls(self, self.ahb_ap, name, addr, *args)

        self.flash = self.devs['FLASH']
        MemDevice(self, self.ahb_ap, 'FBANKS', self.flash.mem_base,
                  self.flash.flash_size)

    def __repr__(self):
        return 'STM32H7xx DP MCU_IDCODE 0x%08X' % self.mcu_idcode

    @staticmethod
    def probe(db):
        # APSEL 0, 2 and 3 should be populated.
        # AP0 is the Cortex-M7 and corresponds with db.cpus[0].
        # AP3 is the Cortex-M4 and corresponds with db.cpus[1].
        if 0 not in db.aps:
            return None
        if 2 not in db.aps:
            return None
        if 3 not in db.aps:
            return None
        if db.cpus[0].ap != db.aps[0]:
            return None
        if db.cpus[1].ap != db.aps[3]:
            return None

        # APSEL 0 and 3 should be an AHB AP.
        for ap in (db.aps[0], db.aps[3]):
            if not isinstance(ap, psdb.access_port.AHBAP):
                return None

        # APSEL 2 should be an APB AP.
        if not isinstance(db.aps[2], psdb.access_port.APBAP):
            return None

        # Identify the STM32H7 through the base component's CIDR/PIDR
        # registers.
        for ap in (db.aps[0], db.aps[2], db.aps[3]):
            c = ap.base_component
            if not c or c.cidr != 0xB105100D or c.pidr != 0x00000000000A0450:
                return None

        # There should be exactly two CPUs.
        if len(db.cpus) != 2:
            return None

        # Finally, we can match on the DBGMCU IDC value.
        rt1 = db.aps[2].base_component.find_components_by_type(STM32H7ROMTable1)
        assert len(rt1) == 1
        if (rt1[0].read_dbgmcu_idc() & 0x00000FFF) != 0x450:
            return None

        return STM32H7_DP(db)
