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
- [x] HC32L110x4xx/HC32F003x4xx
- [x] HC32L110x6xx/HC32F005x6xx


### Hack Tools
* HDSC ISP V2.21, hdsc.exe
* ILSpy
* Logic


### TODO
* More device test
