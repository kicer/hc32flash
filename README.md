# HC32FLASH
HC32xx flash downloader with USB-TTL adapter.


### Usage
```
usage: hc32flash.py [-h] [-l] [-d  device] [-p  port] [-b  baudrate] [-u] [-L]
                    [-R] [-w <filename>] [-r <filename>] [-v <filename>]

HC32xx Flash Downloader.

optional arguments:
  -h, --help     show this help message and exit
  -l, --list     List support device
  -d  device     Device name, default HC32F003
  -p  port       Serial port, default /dev/ttyUSB0
  -b  baudrate   Serial baudrate
  -u, --unlock   Unlock. Erase device when locked
  -L, --lock     Lock. SWD port disabled
  -R, --reboot   Reboot device
  -w <filename>  Write data from file to device
  -r <filename>  Read data from device to file
  -v <filename>  Verify chksum data in device against file
```


### Tested Device
- [ ] HC32D391
- [ ] HC32F4A0
- [ ] HC32F146x8/HC32M140x8
- [ ] HC32F146xA/HC32M140xA
- [ ] HC32F120
- [ ] HC32F460xExx
- [ ] HC32L13xx8/HC32F030x8
- [ ] HC32L15xx8
- [ ] HC32L15xxA
- [x] HC32L110x4xx/HC32F003x4xx
- [x] HC32L110x6xx/HC32F005x6xx
- [ ] HC32M120
- [ ] HC32x19xxCxx
- [ ] HC32x07xxAxx/HC32x17xxAxx



### Hack Tools
* HDSC ISP V2.07, hdsc.exe
* ILSpy
* Logic


### TODO
* Some device need Crystal Freq setting to load ramcode
* Auto Number function
* More device test
