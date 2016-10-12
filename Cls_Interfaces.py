from _winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx
import netifaces
import sys

class Cls_Interface(object):
    def __init__(self):
        myDevices = []

    def get_myDevices(self):
        '''try:
            myDevices = pcapy.findalldevs()
            print "Makinedeki interfaceler ;"

            i = 1
            for d in myDevices:
                print "%s).  %s" % (i, QueryValueEx(d, 'Name')[0])

                i += 1
            return myDevices
        except:
            print "Interfaceler listelenirken hata olustu."
            sys.exit()
        '''
        try:
            try:
                myDevices = netifaces.interfaces()
            except:
                print "Interfaceler listelenirken hata olustu. >> %s", sys.exc_info()
                sys.exit()

            try:
                iface_names = ['(unknown)' for i in range(len(myDevices))]
                reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                reg_key = OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')

                for i in range(len(myDevices)):
                    try:
                        reg_subkey = OpenKey(reg_key, myDevices[i] + r'\Connection')
                        print "\\Device\\NPF_" + myDevices[i] + " = " + QueryValueEx(reg_subkey, 'Name')[0]
                    except:
                        pass
            except:
                print "Interfacelere isim verilirken hata olustu. >> %s", sys.exc_info()

            for i, dev in enumerate(myDevices):
                myDevices[i] = "\\Device\\NPF_" + dev
            return  myDevices

        except:
            print "Interfaceler listelenirken hata olustu.>> %s", sys.exc_info()
            sys.exit()
