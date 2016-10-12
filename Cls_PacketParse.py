import pcapy
import socket
from _winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx
import netifaces
import sys
from struct import *

class Cls_PacketParse(object):
    # Convert a string of 6 characters of ethernet address into a dash separated hex string
    def convert_eth_addr(a):
        b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]), ord(a[1]), ord(a[2]), ord(a[3]), ord(a[4]), ord(a[5]))
        return b

    # function to parse a packet
    def parse_packet(packet):
        # parse ethernet header
        eth_length = 14

        eth_header = packet[:eth_length]
        eth = unpack('!6s6sH', eth_header)
        eth_protocol = socket.ntohs(eth[2])
        print 'ethernet________________'
        print 'Destination MAC : ' + convert_eth_addr(packet[0:6])
        print 'Source MAC : ' + convert_eth_addr(packet[6:12])
        print 'Protocol : ' + str(eth_protocol)

        # Parse IP packets, IP Protocol number = 8
        if eth_protocol == 8:
            # Parse IP header
            # take first 20 characters for the ip header
            ip_header = packet[eth_length:20 + eth_length]

            # now unpack them :)
            iph = unpack('!BBHHHBBH4s4s', ip_header)

            version_ihl = iph[0]
            version = version_ihl >> 4
            ihl = version_ihl & 0xF

            iph_length = ihl * 4

            ttl = iph[5]
            protocol = iph[6]
            s_addr = socket.inet_ntoa(iph[8]);
            d_addr = socket.inet_ntoa(iph[9]);

            print 'ip________________'
            print 'Version : ' + str(version)
            print 'IP Header Length : ' + str(ihl)
            print 'TTL : ' + str(ttl)
            print 'Protocol : ' + str(protocol)
            print 'Source Address : ' + str(s_addr)
            print 'Destination Address : ' + str(d_addr)

            # TCP protocol
            if protocol == 6:
                t = iph_length + eth_length
                tcp_header = packet[t:t + 20]

                # now unpack them :)
                tcph = unpack('!HHLLBBHHH', tcp_header)

                source_port = tcph[0]
                dest_port = tcph[1]
                sequence = tcph[2]
                acknowledgement = tcph[3]
                doff_reserved = tcph[4]
                tcph_length = doff_reserved >> 4

                print 'tcp________________'
                print 'Source Port : ' + str(source_port)
                print 'Dest Port : ' + str(dest_port)
                print 'Sequence Number : ' + str(sequence)
                print 'Acknowledgement : ' + str(acknowledgement)
                print 'TCP header length : ' + str(tcph_length)

                h_size = eth_length + iph_length + tcph_length * 4
                data_size = len(packet) - h_size

                # get data from the packet
                data = packet[h_size:]

                print 'Data : ' + data

            # ICMP Packets
            elif protocol == 1:
                u = iph_length + eth_length
                icmph_length = 4
                icmp_header = packet[u:u + 4]

                # now unpack them :)
                icmph = unpack('!BBH', icmp_header)

                icmp_type = icmph[0]
                code = icmph[1]
                checksum = icmph[2]

                print 'icmp________________'
                print 'Type : ' + str(icmp_type)
                print 'Code : ' + str(code)
                print 'Checksum : ' + str(checksum)

                h_size = eth_length + iph_length + icmph_length
                data_size = len(packet) - h_size

                # get data from the packet
                data = packet[h_size:]

                print 'Data : ' + data

            # UDP packets
            elif protocol == 17:
                u = iph_length + eth_length
                udph_length = 8
                udp_header = packet[u:u + 8]

                # now unpack them :)
                udph = unpack('!HHHH', udp_header)

                source_port = udph[0]
                dest_port = udph[1]
                length = udph[2]
                checksum = udph[3]

                print 'udp________________'
                print 'Source Port : ' + str(source_port)
                print 'Dest Port : ' + str(dest_port)
                print 'Length : ' + str(length)
                print 'Checksum : ' + str(checksum)

                h_size = eth_length + iph_length + udph_length
                data_size = len(packet) - h_size

                # get data from the packet
                data = packet[h_size:]

                print 'Data : ' + data

            # some other IP packet like IGMP
            else:
                print 'Protocol other than TCP/UDP/ICMP'

            print "********************************************************************************"