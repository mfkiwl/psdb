# Copyright (c) 2018-2019 Phase Advanced Sensor Systems, Inc.
from ..device import Device, Reg32, Reg32R, Reg32W
from ..flash import Flash


class FlashBank(Device):
    '''
    Driver for a single flash bank.
    '''
    REGS = [Reg32W('KEYR',      0x004),
            Reg32 ('CR',        0x00C),
            Reg32 ('SR',        0x010),
            Reg32W('CCR',       0x014),
            Reg32R('PRAR_CUR',  0x028),
            Reg32 ('PRAR_PRG',  0x02C),
            Reg32R('SCAR_CUR',  0x030),
            Reg32 ('SCAR_PRG',  0x034),
            Reg32R('WPSN_CURR', 0x038),
            Reg32 ('WPSN_PRGR', 0x03C),
            Reg32 ('CRCCR',     0x050),
            Reg32 ('CRCSADDR',  0x054),
            Reg32 ('CRCEADDR',  0x058),
            Reg32R('ECC_FAR',   0x060),
            ]

    def __init__(self, flash, bank_num):
        Device.__init__(self, flash.target, flash.dev_base + 0x100*bank_num,
                        '%s.%u' % (flash.name, bank_num), FlashBank.REGS)

    def _clear_errors(self):
        self._write_ccr(0x0FEF0000)

    def _check_errors(self):
        v = self._read_sr()
        if v & 0x0FEE0000:
            raise Exception('Flash operation failed, FLASH_SR=0x%08X' % v)

    def _wait_prg_idle(self):
        while self._read_sr() & 7:
            pass

    def _pg_unlock(self):
        v = self._read_cr()
        if v & 1:
            self._write_keyr(0x45670123)
            self._write_keyr(0xCDEF89AB)
            v = self._read_cr()
            assert not (v & 1)
        if not (v & 2):
            self._write_cr(v | 2)

        return self

    def _pg_lock(self):
        v = self._read_cr()
        self._write_cr((v & ~2) | 1)


class UnlockedContextManager(object):
    def __init__(self, bank):
        self.bank = bank

    def __enter__(self):
        self.bank._pg_unlock()
        return self

    def __exit__(self, type, value, traceback):
        self.bank._pg_lock()


class FLASH(Device, Flash):
    '''
    Driver for the FLASH device on the STM32H7xx series of MCUs.
    '''
    REGS = [Reg32 ('ACR',           0x000),
            Reg32W('KEYR1',         0x004),
            Reg32W('OPTKEYR',       0x008),
            Reg32 ('CR1',           0x00C),
            Reg32 ('SR1',           0x010),
            Reg32W('CCR1',          0x014),
            Reg32 ('OPTCR',         0x018),
            Reg32 ('OPTSR_CUR',     0x01C),
            Reg32 ('OPTSR_PRG',     0x020),
            Reg32 ('OPTCCR',        0x024),
            Reg32R('PRAR_CUR1',     0x028),
            Reg32 ('PRAR_PRG1',     0x02C),
            Reg32R('SCAR_CUR1',     0x030),
            Reg32 ('SCAR_PRG1',     0x034),
            Reg32R('WPSN_CUR1R',    0x038),
            Reg32 ('WPSN_PRG1R',    0x03C),
            Reg32R('BOOT_CURR',     0x040),
            Reg32 ('BOOT_PRGR',     0x044),
            Reg32 ('CRCCR1',        0x050),
            Reg32 ('CRCSADD1R',     0x054),
            Reg32 ('CRCEADD1R',     0x058),
            Reg32R('CRCDATAR',      0x05C),
            Reg32R('ECC_FA1R',      0x060),
            Reg32W('KEYR2',         0x104),
            Reg32 ('CR2',           0x10C),
            Reg32 ('SR2',           0x110),
            Reg32W('CCR2',          0x114),
            Reg32R('PRAR_CUR2',     0x128),
            Reg32 ('PRAR_PRG2',     0x12C),
            Reg32R('SCAR_CUR2',     0x130),
            Reg32 ('SCAR_PRG2',     0x134),
            Reg32R('WPSN_CUR2R',    0x138),
            Reg32 ('WPSN_PRG2R',    0x13C),
            Reg32 ('CRCCR2',        0x150),
            Reg32 ('CRCSADD2R',     0x154),
            Reg32 ('CRCEADD2R',     0x158),
            Reg32R('ECC_FA2R',      0x160),
            ]

    def __init__(self, target, name, dev_base, mem_base):
        sector_size = 128*1024
        Device.__init__(self, target, dev_base, name, FLASH.REGS)
        Flash.__init__(self, mem_base, sector_size,
                       target.flash_size // sector_size)
        nbanks                = 1 if target.flash_size == 128*1024 else 2
        self.banks            = [FlashBank(self, i) for i in range(nbanks)]
        self.sectors_per_bank = self.nsectors // nbanks
        self.bank_size        = self.sector_size * self.sectors_per_bank

    def _flash_bank_unlocked(self, bank):
        return UnlockedContextManager(bank)

    def erase_sector(self, n, verbose=True):
        '''
        Erases the nth sector in flash.
        The sector is verified to be erased before returning.
        '''
        assert 0 <= n and n < self.nsectors

        addr = self.mem_base + n * self.sector_size
        if verbose:
            print('Erasing sector [0x%08X - 0x%08X]...' % (
                    addr, addr + self.sector_size - 1))

        bank = self.banks[n // self.sectors_per_bank]
        with self._flash_bank_unlocked(bank):
            bank._clear_errors()
            v  = bank._read_cr()
            v |= ((n % self.sectors_per_bank) << 8) | (1 << 7) | (1 << 2)
            bank._write_cr(v)
            bank._wait_prg_idle()
            bank._check_errors()

    def read(self, addr, length):
        '''
        Reads a region from the flash.
        '''
        return self.target.ahb_ap.read_bulk(addr, length)

    def write(self, addr, data, verbose=True):
        '''
        Writes 32-byte lines of data to the flash.  The address must be
        32-byte aligned and the data to write must be a multiple of 32 bytes in
        length and should all be contained within one flash bank but may span
        multiple sectors.

        The target region to be written must be in the erased state.
        '''
        assert self.target.is_halted()
        if not data:
            return
        assert len(data) % 32 == 0
        assert addr % 32 == 0
        assert (addr & 0xFFF00000) == ((addr + len(data) - 1) & 0xFFF00000)
        assert self.mem_base <= addr
        assert addr + len(data) <= self.mem_base + self.flash_size

        if verbose:
            print('Flashing region [0x%08X - 0x%08X]...' % (
                    addr, addr + len(data) - 1))

        bank = self.banks[(addr - self.mem_base) // self.bank_size]
        with self._flash_bank_unlocked(bank):
            bank._clear_errors()
            self.target.ahb_ap.write_bulk(data, addr)
            bank._wait_prg_idle()
            bank._check_errors()