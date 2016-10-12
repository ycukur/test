import pcapy
import datetime
from Cls_PacketParse import *

class Cls_PacketCapture(object):
    def packetsCap(device):
        cap = pcapy.open_live(device, 65536, 1, 0)

        # start sniffing packets
        while (1):
            (header, packet) = cap.next()
            print ('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen()))
            inh = Cls_PacketParse()
            inh.parse_packet(packet)