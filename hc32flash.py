import os, sys, time, struct
import serial
import argparse

version = "0.1.2"

HDSC = {
    'HC32D391': {
        'MCUName': "HC32D391",
        'FrequecyList': ["1000000", "500000", "256000", "128000", "115200"],
        'StartAddress': "00000000",
        'PageSize': "8192",
        'PageCount': "64",
        'FlashSize': "512K",
        'BootloaderBaudrate': 115200,
        'RamCodeBinFile': "m_flash.hc010",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(PA13)     <--->    Serial.RXD\nMCU.RXD(PA14)     <--->    Serial.TXD\nMCU.MODE          <--->    MCU.GND\n",
    },
    'HC32F4A0': {
        'MCUName': "HC32F4A0",
        'FrequecyList': ["1000000", "500000", "256000", "128000", "115200"],
        'StartAddress': "00000000",
        'PageSize': "8192",
        'PageCount': "256",
        'FlashSize': "2M",
        'BootloaderBaudrate': 115200,
        'RamCodeBinFile': "m_flash.hc020",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC            <--->    Serial.VCC\nMCU.GND            <--->    Serial.GND\nMCU.TXD(PA13,PB10) <--->    Serial.RXD\nMCU.RXD(PA14,PB11) <--->    Serial.TXD\nMCU.MODE           <--->    MCU.VCC\n",
    },
    'HC32F146x8/HC32M140x8': {
        'MCUName': "HC32F146x8/HC32M140x8",
        'FrequecyList': ["Internal CR", "4MHz", "6MHz", "8MHz", "10MHz", "12MHz", "16MHz", "18MHz", "20MHz", "24MHz", "32MHz"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "128",
        'FlashSize': "64K",
        'BootloaderBaudrate': 9600,
        'RamCodeBinFile': "m_flash.hc001",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(P11)      <--->    Serial.RXD\nMCU.RXD(P12)      <--->    Serial.TXD\nMCU.MODE          <--->    MCU.VCC\n",
    },
    'HC32F146xA/HC32M140xA': {
        'MCUName': "HC32F146xA/HC32M140xA",
        'FrequecyList': ["Internal CR", "4MHz", "6MHz", "8MHz", "10MHz", "12MHz", "16MHz", "18MHz", "20MHz", "24MHz", "32MHz"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "256",
        'FlashSize': "128K",
        'BootloaderBaudrate': 9600,
        'RamCodeBinFile': "m_flash.hc001",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(P11)      <--->    Serial.RXD\nMCU.RXD(P12)      <--->    Serial.TXD\nMCU.MODE          <--->    MCU.VCC\n",
    },
    'HC32F120': {
        'MCUName': "HC32F120",
        'FrequecyList': ["1000000"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "64",
        'FlashSize': "32K",
        'BootloaderBaudrate': 1000000,
        'RamCodeBinFile': "m_flash.hc012",
        'WritePacketSize': 512,
        'IspConnection': "请确认目标芯片与转接板的连接：\n半双工：VCC,GND,TOOL0,NRST\n全双工：VCC,GND,TXD,RXD,TOOL0,NRST\n",
    },
    'HC32F460xExx': {
        'MCUName': "HC32F460xExx",
        'FrequecyList': ["1000000", "500000", "256000", "128000", "115200"],
        'StartAddress': "00000000",
        'PageSize': "8192",
        'PageCount': "64",
        'FlashSize': "512K",
        'BootloaderBaudrate': 115200,
        'RamCodeBinFile': "m_flash.hc010",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(PA13)     <--->    Serial.RXD\nMCU.RXD(PA14)     <--->    Serial.TXD\nMCU.MODE          <--->    MCU.GND\n",
    },
    'HC32L13xx8/HC32F030x8': {
        'MCUName': "HC32L13xx8/HC32F030x8",
        'FrequecyList': ["1000000", "256000", "128000", "115200", "76800", "38400", "19200", "9600"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "128",
        'FlashSize': "64K",
        'BootloaderBaudrate': 9600,
        'RamCodeBinFile': "m_flash.hc006",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(PA09/PA14)<--->    Serial.RXD\nMCU.RXD(PA10/PA13)<--->    Serial.TXD\nMCU.MODE          <--->    MCU.VCC\n",
    },
    'HC32L15xx8': {
        'MCUName': "HC32L15xx8",
        'FrequecyList': ["Internal CR", "4MHz", "6MHz", "8MHz", "10MHz", "12MHz", "16MHz", "18MHz", "20MHz", "24MHz", "32MHz"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "128",
        'FlashSize': "64K",
        'BootloaderBaudrate': 9600,
        'RamCodeBinFile': "m_flash.hc001",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(P12)      <--->    Serial.RXD\nMCU.RXD(P11)      <--->    Serial.TXD\nMCU.MODE          <--->    MCU.VCC\n",
    },
    'HC32L15xxA': {
        'MCUName': "HC32L15xxA",
        'FrequecyList': ["Internal CR", "4MHz", "6MHz", "8MHz", "10MHz", "12MHz", "16MHz", "18MHz", "20MHz", "24MHz", "32MHz"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "256",
        'FlashSize': "128K",
        'BootloaderBaudrate': 9600,
        'RamCodeBinFile': "m_flash.hc001",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(P12)      <--->    Serial.RXD\nMCU.RXD(P11)      <--->    Serial.TXD\nMCU.MODE          <--->    MCU.VCC\n",
    },
    'HC32L110x4xx/HC32F003x4xx': {
        'MCUName': "HC32L110x4xx/HC32F003x4xx",
        'FrequecyList': ["691200", "230400", "115200", "38400", "19200", "9600"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "32",
        'FlashSize': "16K",
        'BootloaderBaudrate': 9600,
        'RamCodeBinFile': "m_flash.hc005",
        'WritePacketSize': 64,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(P31/P35)  <--->    Serial.RXD\nMCU.RXD(P27/P36)  <--->    Serial.TXD\nMCU.RESET         <--->    Serial.RTS/DTR\n",
    },
    'HC32L110x6xx/HC32F005x6xx': {
        'MCUName': "HC32L110x6xx/HC32F005x6xx",
        'FrequecyList': ["691200", "460800", "230400", "115200", "38400", "19200", "9600"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "64",
        'FlashSize': "32K",
        'BootloaderBaudrate': 9600,
        'RamCodeBinFile': "m_flash.hc005",
        'WritePacketSize': 64,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(P31/P35)  <--->    Serial.RXD\nMCU.RXD(P27/P36)  <--->    Serial.TXD\nMCU.RESET         <--->    Serial.RTS/DTR\n",
    },
    'HC32M120': {
        'MCUName': "HC32M120",
        'FrequecyList': ["1000000"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "32",
        'FlashSize': "16K",
        'BootloaderBaudrate': 1000000,
        'RamCodeBinFile': "m_flash.hc013",
        'WritePacketSize': 512,
        'IspConnection': "请确认目标芯片与转接板的连接：\n半双工：VCC,GND,TOOL0,NRST\n全双工：VCC,GND,TXD,RXD,TOOL0,NRST\n",
    },
    'HC32x19xxCxx': {
        'MCUName': "HC32x19xxCxx",
        'FrequecyList': ["1000000", "256000", "128000", "115200", "76800", "38400", "19200"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "512",
        'FlashSize': "256K",
        'BootloaderBaudrate': 115200,
        'RamCodeBinFile': "m_flash.hc015",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(PA14)     <--->    Serial.RXD\nMCU.RXD(PA13)     <--->    Serial.TXD\nMCU.BOOT0         <--->    MCU.VCC\n",
    },
    'HC32x07xxAxx/HC32x17xxAxx': {
        'MCUName': "HC32x07xxAxx/HC32x17xxAxx",
        'FrequecyList': ["1000000", "256000", "128000", "115200", "76800", "38400", "19200"],
        'StartAddress': "00000000",
        'PageSize': "512",
        'PageCount': "256",
        'FlashSize': "128K",
        'BootloaderBaudrate': 115200,
        'RamCodeBinFile': "m_flash.hc008",
        'WritePacketSize': 512,
        'IspConnection': "MCU.VCC           <--->    Serial.VCC\nMCU.GND           <--->    Serial.GND\nMCU.TXD(PA14)     <--->    Serial.RXD\nMCU.RXD(PA13)     <--->    Serial.TXD\nMCU.BOOT0         <--->    MCU.VCC\n",
    },
}


class TransportError(Exception):
    """Custom exception to represent errors with a transport
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SerialTransport():
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.serial = None

        try:
            self.serial = serial.Serial(port, baud)
        except serial.SerialException as e:
            raise TransportError(str(e)) from None

        self.serial.timeout = 1
        self.serial.write_timeout = None

    def init_baud(self, baud):
        self.serial.baudrate = baud

    def write(self, data, flush=True):
        if self.serial.inWaiting() > 0:
            self.serial.flushInput()
        self.serial.write(data)
        if flush: self.serial.flush()

    def read(self, length):
        return self.serial.read(length)

    def close(self):
        self.serial.flush()
        self.serial.close()

    def goto_bootloader(self):
        self.serial.rts = True
        time.sleep(0.1)
        self.write(b'\x18\xFF'*10, flush=False)
        self.serial.rts = False
        ack = self.read(10)
        return ack[-6:] == b'\x11'*6

    def check_lock(self):
        self.write(b'\x01\xFC\x0B\x00\x00\x02\x00\x00\x00\x0A')
        ack = self.read(5)
        if len(ack)==5 and ack[:2]==b'\x01\x02':
            return ack[2:4] != b'\xFF\xFF'
        return None

    def unlock(self):
        self.write(b'\xB5\x34\x84\x52\xBF')
        return self.read(1) == b'\x01'

    def load_ramcode(self, _f):
        with open(_f, "rb") as fr:
            dat = fr.read()
            fr.close()
            size = len(dat)
            addr = 0x20000000
            pkg = struct.pack('<b2I',0,addr,size)
            chksum = bytes([sum(pkg)&0xFF])
            self.write(pkg+chksum)
            if self.read(1) == b'\x01':
                cnt = self.write(dat + bytes([sum(dat)&0xFF]))
                return self.read(1) == b'\x01'
        return False

    def run_ramcode(self):
        self.write(b'\xC0\x00\x00\x00\x00\x00\x00\x00\x00\xC0')
        return repr(self.read(11))

    def ramcode_api(self, cmd, addr, dat, size=0):
        size = size or len(dat)
        pkg = bytes([0x49,cmd]) + struct.pack('<IH',addr,size) + dat
        return pkg + bytes([sum(pkg)&0xFF])

    def set_baud(self, baud):
        self.write(self.ramcode_api(0x01, 0, struct.pack('<I',baud)))
        ack = self.ramcode_api(0x00, 0, b'')
        return self.read(9) == ack

    def flash_erase(self):
        self.write(self.ramcode_api(0x02,0,b''))
        ack = self.ramcode_api(0x00, 0, b'')
        return self.read(9) == ack

    def flash_write(self, addr, dat):
        self.write(self.ramcode_api(0x04, addr, dat))
        ack = self.ramcode_api(0x00, addr, b'')
        self.serial.flush()
        return self.read(9) == ack

    def flash_read(self, addr, size):
        dat = None; psize = 9+size
        self.write(self.ramcode_api(0x05, addr, b'', size))
        ack = self.read(psize)
        if len(ack)==(psize) and (sum(ack[:-1])&0xFF)==ack[-1]:
            dat = ack[8:8+size]
        return dat

    def flash_verify(self, size):
        self.write(self.ramcode_api(0x06, 0, struct.pack('<I',size)))
        ack = self.read(11)
        if len(ack)==11 and (sum(ack[:-1])&0xFF)==ack[-1]:
            return ack[8:10]
        return None

    def flash_lock(self):
        self.write(self.ramcode_api(0x09, 0, b''))
        ack = self.ramcode_api(0x00, 0, b'')
        return self.read(9) == ack

    def reboot(self):
        self.serial.rts = True
        time.sleep(0.1)
        self.serial.rts = False
        return True


if __name__ == '__main__':
    # parse arguments or use defaults
    parser = argparse.ArgumentParser(description='HC32xx Flash Downloader.')
    parser.add_argument('-l', '--list', action='store_true', help='List support device')
    parser.add_argument('-d', metavar=' device', default='HC32F003', help='Device name, default HC32F003')
    parser.add_argument('-p', metavar=' port', default='/dev/ttyUSB0', help='Serial port, default /dev/ttyUSB0')
    parser.add_argument('-b', metavar=' baudrate',type=int,default=0, help='Serial baudrate')
    parser.add_argument('-u', '--unlock', action='store_true', help='Unlock. Erase device when locked')
    parser.add_argument('-L', '--lock', action='store_true', help='Lock. SWD port disabled')
    parser.add_argument('-R', '--reboot', action='store_true', help='Reboot device')
    parser.add_argument('-e', '--erase', action='store_true', help='Erase device')
    parser.add_argument('-w', metavar='<filename>', help='Write data from file to device')
    parser.add_argument('-r', metavar='<filename>', help='Read data from device to file')
    parser.add_argument('-v', metavar='<filename>', help='Verify chksum data in device against file')
    args = parser.parse_args()

    args.dev,args.port,args.baud = args.d,args.p,args.b
    args.rfile,args.wfile,args.vfile = args.r,args.w,args.v

    # check device
    _ = None
    for dev in HDSC.keys():
        if dev.find(args.dev.upper()) >= 0:
            args.dev,_ = dev,dev
            break
    if not _:
        sys.stdout.write("Invalid Device name '%s'.\n\nList of support device:\n" % args.dev)
        args.list = True

    if args.list:
        for dev in HDSC.keys():
            sys.stdout.write("%-28s %-8s %s\n" % (dev, HDSC[dev]['FlashSize'], HDSC[dev]['BootloaderBaudrate']))
        sys.exit(0)

    # mcu info
    hc32xx =  HDSC[args.dev]
    args.baud = args.baud or hc32xx['BootloaderBaudrate']
    sys.stdout.write('Device:     %s\n' % args.dev)
    sys.stdout.write('Boot Baud:  %s\n' % args.baud)
    sys.stdout.write('Page Size:  %s\n' % hc32xx['PageSize'])
    sys.stdout.write('Page Count: %s\n' % hc32xx['PageCount'])
    sys.stdout.write('Flash Size: %s\n' % hc32xx['FlashSize'])
    #sys.stdout.write('RameCode:   %s\n' % hc32xx['RamCodeBinFile'])
    sys.stdout.write('\n%s\n' % hc32xx['IspConnection'])
    # global vars
    transport = SerialTransport(args.port, hc32xx['BootloaderBaudrate'])
    base_dir = os.path.dirname(os.path.realpath(__file__))

    # stage 1. goto bootload
    sys.stdout.write("Stage 1. Goto bootloader: ")
    sys.stdout.flush()
    if transport.goto_bootloader():
        sys.stdout.write("succ\n")
    else:
        sys.stdout.write("error\n")
        sys.exit(1)

    # state 2. Check device
    sys.stdout.write("Stage 2. Check device: ")
    if transport.check_lock():
        if args.unlock and transport.unlock():
            sys.stdout.write("unlock\n")
        else:
            sys.stdout.write("%s\n" % args.unlock and "locked" or "unlock failed")
            sys.exit(1)
    else:
        sys.stdout.write("pass\n")

    # stage 3. load ramcode
    sys.stdout.write("Stage 3. Load ramcode: ")
    sys.stdout.flush()
    _f = os.path.join(base_dir, 'hdsc', 'HDSC.'+hc32xx['RamCodeBinFile'])
    if transport.load_ramcode(_f):
        sys.stdout.write("%s\n" % hc32xx['RamCodeBinFile'])
    else:
        sys.stdout.write("error\n")
        sys.exit(1)

    # stage 4. run ramcode
    sys.stdout.write("Stage 4. Run ramcode: %s\n" %
        transport.run_ramcode())

    # stage 5. set baud
    sys.stdout.write("Stage 5. Set baud: ")
    if transport.set_baud(args.baud):
        sys.stdout.write("%s\n\n" % args.baud)
        transport.init_baud(args.baud)
    else:
        sys.stdout.write("error\n")
        sys.exit(1)

    # erase device
    if args.erase or args.wfile:
        sys.stdout.write("[ ERASE] %s\n" %
            (transport.flash_erase() and 'ok' or 'error'))

    # write, with erase
    if args.wfile:
        with open(args.wfile, "rb") as fs:
            sys.stdout.write("[ WRITE] ")
            psize = int(hc32xx['WritePacketSize'])
            addr0 = int(hc32xx['StartAddress'], 16)
            addr = addr0
            while True:
                _last = False
                dat = fs.read(psize)
                if len(dat) == 0:
                    _last = True
                else:
                    if len(dat) < psize:
                        dat = dat + b'\xFF'*(psize-len(dat))
                        _last = True
                    if transport.flash_write(addr, dat):
                        sys.stdout.write("."); sys.stdout.flush()
                    else:
                        sys.stdout.write("flash write error: 0x%08X\n" % addr)
                        sys.exit(1)
                addr += psize
                if _last:
                    sys.stdout.write(" ok\n")
                    fs.close()
                    if not args.vfile:
                        args.vfile = args.wfile
                    break

    # read to file
    if args.rfile:
        with open(args.rfile, "wb") as fs:
            sys.stdout.write("[ READ ] ")
            psize = int(hc32xx['PageSize'])
            pcnt = int(hc32xx['PageCount'])
            addr0 = int(hc32xx['StartAddress'], 16)
            addr = addr0
            for _ in range(pcnt):
                dat = transport.flash_read(addr, psize)
                if not dat:
                    sys.stdout.write("flash read error: 0x%08X\n" % addr)
                    sys.exit(1)
                else:
                    fs.write(dat)
                    sys.stdout.write("."); sys.stdout.flush()
                addr += psize
            sys.stdout.write(" ok\n")
            fs.close()

    # verify chksum
    if args.vfile:
        with open(args.vfile, "rb") as fs:
            sys.stdout.write("[VERIFY] ")
            dat = fs.read()
            fs.close()
            ack = transport.flash_verify(len(dat))
            chk0,chk1 = sum(dat)&0xFFFF,None
            if ack:
                chk1 = struct.unpack('<H',ack)[0]
            if chk0 == chk1:
                sys.stdout.write("0x%04X, ok\n" % chk0)
            else:
                sys.stdout.write("flash verify error: %s/%s\n" % (chk0, chk1))

    # lock device
    if args.lock:
        sys.stdout.write("[ LOCK ] %s\n" %
            (transport.flash_lock() and 'ok' or 'error'))

    # reboot
    if args.reboot:
        sys.stdout.write("[REBOOT] %s\n" %
            (transport.reboot() and 'ok' or 'error'))

    transport.close()
    sys.exit(0)
