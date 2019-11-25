import usb
from . import stlink
from . import cdb


class STLinkV3E(stlink.STLink):
    '''
    STLink V3E debug probe.  This can be found on the Nucleo 64 board we have
    for the STM32G475 chip.
    '''
    def __init__(self, usb_dev):
        super(STLinkV3E, self).__init__(usb_dev, 'STLinkV3E')
        self._usb_version()
        assert self.ver_stlink == 3

        self.max_rw8        = 512
        self.features      |= stlink.FEATURE_BULK_READ_16
        self.features      |= stlink.FEATURE_BULK_WRITE_16
        self.features      |= stlink.FEATURE_RW_STATUS_12
        self._swd_freqs_khz = sorted(self._get_com_freq(), reverse=True)

    def _usb_last_xfer_status(self):
        '''
        Returns a 12-byte transfer status; the error code is in the first byte.
        '''
        return self._usb_xfer_in(cdb.LastXFERStatus12.make(), 12)

    def _usb_version(self):
        rsp = self._usb_xfer_in(cdb.Version2.make(), 12)
        (self.ver_stlink,
         self.ver_swim,
         self.ver_jtag,
         self.ver_msd,
         self.ver_bridge,
         self.ver_vid,
         self.ver_pid) = cdb.Version2.decode(rsp)

    def _read_dpidr(self):
        rsp = self._cmd_allow_retry(cdb.ReadIDCodes.make(), 12)
        return cdb.ReadIDCodes.decode(rsp)[0]

    def _get_com_freq(self, is_jtag=False):
        '''
        Returns the list of supported frequencies, in kHz.
        '''
        cmd   = cdb.GetComFreqs.make(is_jtag)
        rsp   = self._cmd_allow_retry(cmd, cdb.GetComFreqs.RSP_LEN)
        return cdb.GetComFreqs.decode(rsp)

    def _set_com_freq(self, freq_khz, is_jtag=False):
        '''
        Sets the communication frequency to the highest supported frequency
        that doesn't exceed the requested one.  Returns the actual frequency in
        kHz.
        '''
        cmd = cdb.SetComFreq.make(freq_khz, is_jtag)
        try:
            rsp = self._cmd_allow_retry(cmd, 8)
            return cdb.SetComFreq.decode(rsp)
        except stlink.STLinkCmdException as e:
            if e.err != 0x08:
                raise
        if is_jtag:
            raise Exception('Requested JTAG frequency %u kHz too low.'
                            % freq_khz)
        raise Exception('Requested SWD frequency %u kHz too low; minimum is '
                        '%u kHz.' % (freq_khz, self._swd_freqs_khz[-1]))

    def set_tck_freq(self, freq_hz):
        '''
        Sets the communication frequency to the highest supported frequency
        that doesn't exceed the requested one.  Returns the actual frequency in
        Hz.
        '''
        return self._set_com_freq(freq_hz // 1000, is_jtag=False) * 1000

    def show_info(self):
        super(STLinkV3E, self).show_info()
        print(' Firmware Ver: V%uJ%uM%uB%uS%u' % (
            self.ver_stlink, self.ver_jtag, self.ver_msd, self.ver_bridge,
            self.ver_swim))


def enumerate():
    devices = usb.core.find(find_all=True, idVendor=0x0483, idProduct=0x374E)
    return [STLinkV3E(d) for d in devices]