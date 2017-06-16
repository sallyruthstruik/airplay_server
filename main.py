
#!/usr/bin/env python

""" Example of announcing a service (in this case, a fake HTTP server) """

import logging
import socket
import sys
from time import sleep

from zeroconf import ServiceInfo, Zeroconf

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    desc = {
        "ft": "0xA7FFFF7,0xE",
        "pt": "0",
        "am": "VirtualBox (innotek GmbH )",
        "vs": "5.3.2",
        "pf": "Microsoft Windows 7 Home Premium",
        "deviceid": "08:00:27:7B:DE:F3",
        "pk": "96c57560c07e592c3276edd81aac695be11d148d45349e09b4660ec5ac11e4f3",
        "pi": "FC1990B7-A5E1-4A2F-9B39-9628E0662306",
        "os": "6.1.7601",
        "sf": "0x4"
    }

    info = ServiceInfo(
        "_airserver._tcp.local.",
        "Test-PC._airserver._tcp.local.",
        socket.inet_aton("192.168.0.109"), 7000, 2, 2, properties=desc,
        server="Test-PC.local."
    )

    airplay_desc = {
        "features": "0xA7FFFF7,0xE",
        "srcvers": "220.68",
        "flags": "0x4",
        "deviceid": "08:00:27:7B:DE:F3",
        "vv": "2",
        "pk": "96c57560c07e592c3276edd81aac695be11d148d45349e09b4660ec5ac11e4f3",
        "model": "AppleTV5,3",
        "pi": "FC1990B7-A5E1-4A2F-9B39-9628E0662306"
    }

    airplay = ServiceInfo(
        "_airplay._tcp.local.",
        "Test-PC._airplay._tcp.local.",
        socket.inet_aton("192.168.0.109"), 7000, 2, 2, properties=airplay_desc,
        server="Test-PC.local."
    )


    raop_desc = {
        "md": "0,1,2",
        "ft": "0xA7FFFF7,0xE",
        "cn": "0,1,2,3",
        "am": "AppleTV5,3",
        "tp": "UDP",
        "da": "true",
        "vs": "220.68",
        "vn": "65537",
        "vv": "2",
        "et": "0,3,5",
        "pk": "96c57560c07e592c3276edd81aac695be11d148d45349e09b4660ec5ac11e4f3",
        "sf": "0x4"
    }
    raop = ServiceInfo(
        "_raop._tcp.local.",
        "0800277BDEF3@Test-PC._raop._tcp.local.",
        socket.inet_aton("192.168.0.109"), 5000, 2, 2, properties=raop_desc,
        server="Test-PC.local."
    )

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    zeroconf.register_service(airplay)
    zeroconf.register_service(raop)
    print("Service registered!")

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_all_services()
        zeroconf.close()