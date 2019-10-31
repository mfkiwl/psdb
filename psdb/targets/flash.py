# Copyright (c) 2019 Phase Advanced Sensor Systems, Inc.
from .device import Device
from ..block import RAMBD, BlockOutOfRangeException

import math
import time
from builtins import range


class FlashException(Exception):
    pass


class FlashEraseException(Exception):
    pass


class FlashWriteException(Exception):
    pass


class Flash(Device):
    def __init__(self, target, reg_base, name, regs, base_addr):
        super(Flash, self).__init__(target, reg_base, name, regs)
        self.base_addr   = base_addr
        self.sector_size = None
        self.sector_mask = None
        self.flash_size  = None
        self.nsectors    = None

    def _set_geometry(self, sector_size, nsectors):
        self.sector_size = sector_size
        self.sector_mask = sector_size - 1
        self.flash_size  = sector_size * nsectors
        self.nsectors    = nsectors

    def _mask_for_alp(self, addr, length):
        '''
        Returns a bitmask of all sectors containing any part of the specified
        address-length pair.
        '''
        begin    = addr & ~self.sector_mask
        end      = addr + length + (-(addr + length) & self.sector_mask)
        nsectors = (end - begin) // self.sector_size
        fbit     = (begin - self.base_addr) // self.sector_size
        assert 0 <= fbit and fbit < self.nsectors
        assert 0 <= nsectors and fbit + nsectors <= self.nsectors
        return ((1 << nsectors) - 1) << fbit

    def erase_sector(self, n, verbose=True):
        '''
        Erases the nth sector.
        '''
        assert 0 <= n and n < self.nsectors
        raise NotImplementedError

    def erase_sectors(self, mask, verbose=True):
        '''
        Erases the sectors specified in the bit mask.
        '''
        for i in range(int(math.floor(math.log(mask, 2))) + 1):
            if (mask & (1 << i)):
                self.erase_sector(i)

    def erase(self, addr, length, verbose=True):
        '''
        Erases the ALP from the flash.  If the ALP is not perfectly aligned
        to start and end sector boundaries, then the erase operation will also
        erase the edge sectors.
        '''
        return self.erase_sectors(self._mask_for_alp(addr, length),
                                  verbose=verbose)

    def erase_all(self, verbose=True):
        '''
        Erases the entire flash.
        '''
        return self.erase(self.base_addr, self.flash_size, verbose=verbose)

    def read(self, addr, length):
        '''
        Reads a region from the flash.
        '''
        raise NotImplementedError

    def read_all(self):
        '''
        Reads the entire flash.
        '''
        return self.read(self.base_addr, self.flash_size)

    def write(self, addr, data, verbose=True):
        '''
        Writes the specified bytes to the specified address in flash.  The
        region to be written must already be in the erased state.
        '''
        raise NotImplementedError

    def burn_dv(self, dv, verbose=True):
        '''
        Burns the specified data vector to flash, erasing sectors as necessary
        to perform the operation.  The data vector is a list of the form:

            [(address, b'...'),
             (address, b'...'),
             ]

        Data is first prepared in a buffer; earlier vector elements will be
        overwritten by later elements if their ranges overlap.  Flash sectors
        untouched by the data vector are preserved; data between elements
        within a sector is erased.

        Data written to sectors outside flash boundaries is silently discarded.
        '''
        t0 = time.time()

        bd = RAMBD(self.sector_size,
                   first_block=self.base_addr // self.sector_size,
                   nblocks=self.nsectors)
        for v in dv:
            try:
                bd.write(v[0], v[1])
            except BlockOutOfRangeException:
                pass

        mask = 0
        for block in bd.blocks.values():
            mask |= self._mask_for_alp(block.addr, len(block.data))

        total_len = 0
        self.erase_sectors(mask)
        for block in bd.blocks.values():
            while block.data.endswith(b'\xff'*64):
                block.data = block.data[:-64]
            self.write(block.addr, block.data)
            total_len += len(block.data)

        if verbose:
            elapsed = time.time() - t0
            print('Wrote %u bytes in %.2f seconds (%.2f K/s).' %
                  (total_len, elapsed, total_len / (1024*elapsed)))

        t0 = time.time()
        for block in bd.blocks.values():
            if verbose:
                print('Verifying [0x%08X : 0x%08X]...' % (
                      block.addr, block.addr + len(block.data) - 1))
            mem = self.read(block.addr, len(block.data))
            assert mem == block.data
        if verbose:
            elapsed = time.time() - t0
            print('Verified %u bytes in %.2f seconds (%.2f K/s).' %
                  (total_len, elapsed, total_len / (1024*elapsed)))

    def burn_elf(self, elf_bin, verbose=True):
        '''
        Given a psdb.elf.ELFBinary whose layout is appropriate for our target
        device, burn it into flash.  ELF program headers targetting regions
        outside of the flash are ignored.
        '''
        dv = [(s['p_paddr'], s.data() + b'\x00'*(s['p_memsz'] - s['p_filesz']))
               for s in elf_bin.iter_segments() if s['p_type'] == 'PT_LOAD']
        self.burn_dv(dv)
