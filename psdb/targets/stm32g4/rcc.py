# Copyright (c) 2018-2019 Phase Advanced Sensor Systems, Inc.
from ..device import Device, Reg32


ENABLE_BITS = {
    # AHB1
    'DMA1'    : (0x048,  0),
    'DMA2'    : (0x048,  1),
    'DMAMUX'  : (0x048,  2),
    'CORDIC'  : (0x048,  3),
    'FMAC'    : (0x048,  4),
    'FLASH'   : (0x048,  8),
    'CRC'     : (0x048, 12),

    # AHB2
    'GPIOA'   : (0x04C,  0),
    'GPIOB'   : (0x04C,  1),
    'GPIOC'   : (0x04C,  2),
    'GPIOD'   : (0x04C,  3),
    'GPIOE'   : (0x04C,  4),
    'GPIOF'   : (0x04C,  5),
    'GPIOG'   : (0x04C,  6),
    'ADC12'   : (0x04C, 13),
    'ADC345'  : (0x04C, 14),
    'DAC1'    : (0x04C, 16),
    'DAC2'    : (0x04C, 17),
    'DAC3'    : (0x04C, 18),
    'DAC4'    : (0x04C, 16),
    'AES'     : (0x04C, 24),
    'RNG'     : (0x04C, 26),

    # AHB3
    'FMC'     : (0x050,  0),
    'QSPI'    : (0x050,  8),

    # APB1.1
    'TIM2'    : (0x058,  0),
    'TIM3'    : (0x058,  1),
    'TIM4'    : (0x058,  2),
    'TIM5'    : (0x058,  3),
    'TIM6'    : (0x058,  4),
    'TIM7'    : (0x058,  5),
    'CRS'     : (0x058,  8),
    'RTCAPB'  : (0x058, 10),
    'WWDG'    : (0x058, 11),
    'SPI2'    : (0x058, 14),
    'SPI3'    : (0x058, 15),
    'USART2'  : (0x058, 17),
    'USART3'  : (0x058, 18),
    'USART4'  : (0x058, 19),
    'USART5'  : (0x058, 20),
    'I2C1'    : (0x058, 21),
    'I2C2'    : (0x058, 22),
    'USB'     : (0x058, 23),
    'FDCAN'   : (0x058, 25),
    'PWR'     : (0x058, 28),
    'I2C3'    : (0x058, 30),
    'LPTIM1'  : (0x058, 31),

    # APB1.2
    'LPUART1' : (0x05C,  0),
    'I2C4'    : (0x05C,  1),
    'UCPD1'   : (0x05C,  8),

    # APB2
    'SYSCFG'  : (0x060,  0),
    'TIM1'    : (0x060, 11),
    'SPI1'    : (0x060, 12),
    'TIM8'    : (0x060, 13),
    'USART1'  : (0x060, 14),
    'SPI4'    : (0x060, 15),
    'TIM15'   : (0x060, 16),
    'TIM16'   : (0x060, 17),
    'TIM17'   : (0x060, 18),
    'TIM20'   : (0x060, 20),
    'SAI1'    : (0x060, 21),
    'HRTIM1'  : (0x060, 26),
    }


class RCC(Device):
    '''
    Driver for the STM Reset and Clock Control (RCC) device.
    '''
    REGS = [Reg32('CR',         0x000, [('',         8),
                                        ('HSION',    1),
                                        ('HSIKERON', 1),
                                        ('HSIRDY',   1),
                                        ('',         5),
                                        ('HSEON',    1),
                                        ('HSERDY',   1),
                                        ('HSEBYP',   1),
                                        ('CSSON',    1),
                                        ('',         4),
                                        ('PLLON',    1),
                                        ('PLLRDY',   1),
                                        ]),
            Reg32('ICSCR',      0x004, [('',       16),
                                        ('HSICAL',  8),
                                        ('HSITRIM', 7),
                                        ]),
            Reg32('CFGR',       0x008, [('SW',      2),
                                        ('SWS',     2),
                                        ('HPRE',    4),
                                        ('PPRE1',   3),
                                        ('PPRE2',   3),
                                        ('',       10),
                                        ('MCOSEL',  4),
                                        ('MCOPRE',  3),
                                        ]),
            Reg32('PLLCFGR',    0x00C, [('PLLSRC',  2),
                                        ('',        2),
                                        ('PLLM',    4),
                                        ('PLLN',    7),
                                        ('',        1),
                                        ('PLLEN',   1),
                                        ('PLLP',    1),
                                        ('',        2),
                                        ('PLLQEN',  1),
                                        ('PLLQ',    2),
                                        ('',        1),
                                        ('PLLREN',  1),
                                        ('PLLR',    2),
                                        ('PLLPDIV', 5),
                                        ]),
            Reg32('CIER',       0x018, [('LSIRDYIE',   1),
                                        ('LSERDYIE',   1),
                                        ('',           1),
                                        ('HSIRDYIE',   1),
                                        ('HSERDYIE',   1),
                                        ('',           3),
                                        ('LSECSSIE',   1),
                                        ('HSI48RDYIE', 1),
                                        ]),
            Reg32('CIFR',       0x01C, [('LSIRDYF',     1),
                                        ('LSERDYF',     1),
                                        ('',            1),
                                        ('HSIRDYF',     1),
                                        ('HSERDYF',     1),
                                        ('PLLRDYF',     1),
                                        ('',            2),
                                        ('CSSF',        1),
                                        ('LSECSSF',     1),
                                        ('HSI48RDYF',   1),
                                        ]),
            Reg32('CICR',       0x020, [('LSIRDYC',     1),
                                        ('LSERDYC',     1),
                                        ('',            1),
                                        ('HSIRDYC',     1),
                                        ('HSERDYC',     1),
                                        ('PLLRDYC',     1),
                                        ('',            2),
                                        ('CSSC',        1),
                                        ('LSECSSC',     1),
                                        ('HSI48RDYC',   1),
                                        ]),
            Reg32('AHB1RSTR',   0x028, [('DMA1RST',     1),
                                        ('DMA2RST',     1),
                                        ('DMAMUX1RST',  1),
                                        ('CORDICRST',   1),
                                        ('FMACRST',     1),
                                        ('',            3),
                                        ('FLASHRST',    1),
                                        ('',            3),
                                        ('CRCRST',      1),
                                        ]),
            Reg32('AHB2RSTR',   0x02C, [('GPIOARST',    1),
                                        ('GPIOBRST',    1),
                                        ('GPIOCRST',    1),
                                        ('GPIODRST',    1),
                                        ('GPIOERST',    1),
                                        ('GPIOFRST',    1),
                                        ('GPIOGRST',    1),
                                        ('',            6),
                                        ('ADC12RST',    1),
                                        ('ADC345RST',   1),
                                        ('',            1),
                                        ('DAC1RST',     1),
                                        ('DAC2RST',     1),
                                        ('DAC3RST',     1),
                                        ('DAC4RST',     1),
                                        ('',            4),
                                        ('AESRST',      1),
                                        ('',            1),
                                        ('RNGRST',      1),
                                        ]),
            Reg32('AHB3RSTR',   0x030, [('FMCRST',      1),
                                        ('',            7),
                                        ('QSPIRST',     1),
                                        ]),
            Reg32('APB1RSTR1',  0x038, [('TIM2RST',     1),
                                        ('TIM3RST',     1),
                                        ('TIM4RST',     1),
                                        ('TIM5RST',     1),
                                        ('TIM6RST',     1),
                                        ('TIM7RST',     1),
                                        ('',            2),
                                        ('CRSRST',      1),
                                        ('',            5),
                                        ('SPI2RST',     1),
                                        ('SPI3RST',     1),
                                        ('',            1),
                                        ('USART2RST',   1),
                                        ('USART3RST',   1),
                                        ('UART4RST',    1),
                                        ('UART5RST',    1),
                                        ('I2C1RST',     1),
                                        ('I2C2RST',     1),
                                        ('USBRST',      1),
                                        ('',            1),
                                        ('FDCANRST',    1),
                                        ('',            2),
                                        ('PWRRST',      1),
                                        ('',            1),
                                        ('I2C3RST',     1),
                                        ('LPTIM1RST',   1),
                                        ]),
            Reg32('APB1RSTR2',  0x03C, [('LPUART1RST',  1),
                                        ('I2C4RST',     1),
                                        ('',            6),
                                        ('UCPD1RST',    1),
                                        ]),
            Reg32('APB2RSTR',   0x040, [('SYSCFGRST',   1),
                                        ('',            10),
                                        ('TIM1RST',     1),
                                        ('SPI1RST',     1),
                                        ('TIM8RST',     1),
                                        ('USART1RST',   1),
                                        ('SPI4RST',     1),
                                        ('TIM15RST',    1),
                                        ('TIM16RST',    1),
                                        ('TIM17RST',    1),
                                        ('',            1),
                                        ('TIM20RST',    1),
                                        ('SAI1RST',     1),
                                        ('',            4),
                                        ('HRTIM1RST',   1),
                                        ]),
            Reg32('AHB1ENR',    0x048, [('DMA1EN',      1),
                                        ('DMA2EN',      1),
                                        ('DMAMUX1EN',   1),
                                        ('CORDICEN',    1),
                                        ('FMACEN',      1),
                                        ('',            3),
                                        ('FLASHEN',     1),
                                        ('',            3),
                                        ('CRCEN',       1),
                                        ]),
            Reg32('AHB2ENR',    0x04C, [('GPIOAEN',     1),
                                        ('GPIOBEN',     1),
                                        ('GPIOCEN',     1),
                                        ('GPIODEN',     1),
                                        ('GPIOEEN',     1),
                                        ('GPIOFEN',     1),
                                        ('GPIOGEN',     1),
                                        ('',            6),
                                        ('ADC12EN',     1),
                                        ('ADC345EN',    1),
                                        ('',            1),
                                        ('DAC1EN',      1),
                                        ('DAC2EN',      1),
                                        ('DAC3EN',      1),
                                        ('DAC4EN',      1),
                                        ('',            4),
                                        ('AESEN',       1),
                                        ('',            1),
                                        ('RNGEN',       1),
                                        ]),
            Reg32('AHB3ENR',    0x050, [('FMCEN',       1),
                                        ('',            7),
                                        ('QSPIEN',      1),
                                        ]),
            Reg32('APB1ENR1',   0x058, [('TIM2EN',      1),
                                        ('TIM3EN',      1),
                                        ('TIM4EN',      1),
                                        ('TIM5EN',      1),
                                        ('TIM6EN',      1),
                                        ('TIM7EN',      1),
                                        ('',            2),
                                        ('CRSEN',       1),
                                        ('',            1),
                                        ('RTCAPBEN',    1),
                                        ('WWDGEN',      1),
                                        ('',            2),
                                        ('SPI2EN',      1),
                                        ('SPI3EN',      1),
                                        ('',            1),
                                        ('USART2EN',    1),
                                        ('USART3EN',    1),
                                        ('UART4EN',     1),
                                        ('UART5EN',     1),
                                        ('I2C1EN',      1),
                                        ('I2C2EN',      1),
                                        ('USBEN',       1),
                                        ('',            1),
                                        ('FDCANEN',     1),
                                        ('',            2),
                                        ('PWREN',       1),
                                        ('',            1),
                                        ('I2C3EN',      1),
                                        ('LPTIM1EN',    1),
                                        ]),
            Reg32('APB1ENR2',   0x05C, [('LPUART1EN',   1),
                                        ('I2C4EN',      1),
                                        ('',            6),
                                        ('UCPD1EN',     1),
                                        ]),
            Reg32('APB2ENR',    0x060, [('SYSCFGEN',    1),
                                        ('',            10),
                                        ('TIM1EN',      1),
                                        ('SPI1EN',      1),
                                        ('TIM8EN',      1),
                                        ('USART1EN',    1),
                                        ('SPI4EN',      1),
                                        ('TIM15EN',     1),
                                        ('TIM16EN',     1),
                                        ('TIM17EN',     1),
                                        ('',            1),
                                        ('TIM20EN',     1),
                                        ('SAI1EN',      1),
                                        ('',            4),
                                        ('HRTIM1EN',    1),
                                        ]),
            Reg32('AHB1SMENR',  0x068, [('DMA1SMEN',    1),
                                        ('DMA2SMEN',    1),
                                        ('DMAMUX1SMEN', 1),
                                        ('CORDICSMEN',  1),
                                        ('FMACSMEN',    1),
                                        ('',            3),
                                        ('FLASHSMEN',   1),
                                        ('SRAM1SMEN',   1),
                                        ('',            2),
                                        ('CRCSMEN',     1),
                                        ]),
            Reg32('AHB2SMENR',  0x06C, [('GPIOASMEN',   1),
                                        ('GPIOBSMEN',   1),
                                        ('GPIOCSMEN',   1),
                                        ('GPIODSMEN',   1),
                                        ('GPIOESMEN',   1),
                                        ('GPIOFSMEN',   1),
                                        ('GPIOGSMEN',   1),
                                        ('',            2),
                                        ('CCMSRAMSMEN', 1),
                                        ('SRAM2SMEN',   1),
                                        ('',            2),
                                        ('ADC12SMEN',   1),
                                        ('ADC345SMEN',  1),
                                        ('',            1),
                                        ('DAC1SMEN',    1),
                                        ('DAC2SMEN',    1),
                                        ('DAC3SMEN',    1),
                                        ('DAC4SMEN',    1),
                                        ('',            4),
                                        ('AESMEN',      1),
                                        ('',            1),
                                        ('RNGEN',       1),
                                        ]),
            Reg32('AHB3SMENR',  0x070, [('FMCSMEN',     1),
                                        ('',            7),
                                        ('QSPISMEN',    1),
                                        ]),
            Reg32('APB1SMENR1', 0x078, [('TIM2SMEN',    1),
                                        ('TIM3SMEN',    1),
                                        ('TIM4SMEN',    1),
                                        ('TIM5SMEN',    1),
                                        ('TIM6SMEN',    1),
                                        ('TIM7SMEN',    1),
                                        ('',            2),
                                        ('CRSSMEN',     1),
                                        ('',            1),
                                        ('RTCAPBSMEN',  1),
                                        ('WWDGSMEN',    1),
                                        ('',            2),
                                        ('SPI2SMEN',    1),
                                        ('SPI3SMEN',    1),
                                        ('',            1),
                                        ('USART2SMEN',  1),
                                        ('USART3SMEN',  1),
                                        ('UART4SMEN',   1),
                                        ('UART5SMEN',   1),
                                        ('I2C1SMEN',    1),
                                        ('I2C2SMEN',    1),
                                        ('USBSMEN',     1),
                                        ('',            1),
                                        ('FDCANSMEN',   1),
                                        ('',            2),
                                        ('PWRSMEN',     1),
                                        ('',            1),
                                        ('I2C3SMEN',    1),
                                        ('LPTIM1SMEN',  1),
                                        ]),
            Reg32('APB1SMENR2', 0x07C, [('LPUART1SMEN', 1),
                                        ('I2C4SMEN',    1),
                                        ('',            6),
                                        ('UCPD1SMEN',   1),
                                        ]),
            Reg32('APB2SMENR',  0x080, [('SYSCFGSMEN',  1),
                                        ('',            10),
                                        ('TIM1SMEN',    1),
                                        ('SPI1SMEN',    1),
                                        ('TIM8SMEN',    1),
                                        ('USART1SMEN',  1),
                                        ('SPI4SMEN',    1),
                                        ('TIM15SMEN',   1),
                                        ('TIM16SMEN',   1),
                                        ('TIM17SMEN',   1),
                                        ('',            1),
                                        ('TIM20SMEN',   1),
                                        ('SAI1SMEN',    1),
                                        ('',            4),
                                        ('HRTIM1SMEN',  1),
                                        ]),
            Reg32('CCIPR',      0x088, [('USART1SEL',   2),
                                        ('USART2SEL',   2),
                                        ('USART3SEL',   2),
                                        ('UART4SEL',    2),
                                        ('UART5SEL',    2),
                                        ('LPUART1SEL',  2),
                                        ('I2C1SEL',     2),
                                        ('I2C2SEL',     2),
                                        ('I2C3SEL',     2),
                                        ('LPTIM1SEL',   2),
                                        ('SAI1SEL',     2),
                                        ('I2S23SEL',    2),
                                        ('FDCANSEL',    2),
                                        ('CLK48SEL',    2),
                                        ('ADC12SEL',    2),
                                        ('ADC345SEL',   2),
                                        ]),
            Reg32('BDCR',       0x090, [('LSEON',       1),
                                        ('LSERDY',      1),
                                        ('LSEBYP',      1),
                                        ('LSEDRV',      2),
                                        ('LSECSSON',    1),
                                        ('LSECSSD',     1),
                                        ('',            1),
                                        ('RTCSEL',      2),
                                        ('',            5),
                                        ('RTCEN',       1),
                                        ('BDRST',       1),
                                        ('',            7),
                                        ('LSCOEN',      1),
                                        ('LSCOSEL',     1),
                                        ]),
            Reg32('CSR',        0x094, [('LSION',       1),
                                        ('LSIRDY',      1),
                                        ('',            21),
                                        ('RMVF',        1),
                                        ('',            1),
                                        ('OBLRSTF',     1),
                                        ('PINRSTF',     1),
                                        ('BORRSTF',     1),
                                        ('SFTRSTF',     1),
                                        ('IWDGRSTF',    1),
                                        ('WWDGRSTF',    1),
                                        ('LPWRRSTF',    1),
                                        ]),
            Reg32('CRRCR',      0x098, [('HSI48ON',     1),
                                        ('HSI48RDY',    1),
                                        ('',            5),
                                        ('HSI48CAL',    9),
                                        ]),
            Reg32('CCIPR2',     0x09C, [('I2C4SEL',     2),
                                        ('',            18),
                                        ('QSPISEL',     2),
                                        ]),
            ]

    def __init__(self, target, ap, name, addr, **kwargs):
        super(RCC, self).__init__(target, ap, addr, name, RCC.REGS, **kwargs)

    def enable_device(self, name):
        offset, bit = ENABLE_BITS[name]
        if self._get_field(1, bit, offset) == 0:
            self._set_field(1, 1, bit, offset)
