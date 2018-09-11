#!/usr/bin/python3

import threading
from multiping import multi_ping

#-------------------------------------------------------------------------------------------------------------------
# This function increments the ip_address provided
#-------------------------------------------------------------------------------------------------------------------

def increment_addr(self,addr):
    address = list(map( int, addr.split(".")))

    address[3] = address[3]+1
    if address[3]>255:
        address[3] =0
        address[2] = address[2]+1

    if address[2]>255:
        address[2] =0
        address[1] = address[1]+1

    if address[1]>255:
        address[1] =0
        address[0] = address[0]+1

    if address[0]>255:
        address[0] = 0


    return ".".join(list(map(str,address)))




#-------------------------------------------------------------------------------------------------------------------
#               This function compares two ip addresses.
#               if a1 < a2, then it returns 1
#               else if a1 > a2, it returns -1
#               if a1 == a2, it returns 0
#--------------------------------------------------------------------------------------------------------------------

def match_addr(self,a1,a2):
    addr1 = list(map( int, a1.split(".")))
    addr2 = list(map( int, a2.split(".")))

    if addr1[0] == addr2[0]:
        if addr1[1] == addr2[1]:
            if addr1[2] == addr2[2]:
                if addr1[3] == addr2[3]:
                    return 0
                elif addr1[3]>addr2[3]:
                    return -1
                else:
                     return 1
            elif addr1[2] > addr2[2]:
                return -1
            else:
                return 1
        elif addr1[1] > addr2[1]:
            return -1
        else:
             return 1
    elif addr1[0] > addr2[0]:
        return -1
    else:
        return 1





#-------------------------------------------------------------------------------------------------------------------
#               Uses multiping module to send pings
#-------------------------------------------------------------------------------------------------------------------

def send_ping(self,addrs,no_of_retries):

    print("sending again, waiting with retries via provided send_receive()")
    responses, no_response = multi_ping(addrs, timeout=1, retry=2,ignore_lookup_errors=True)
    print("\n\n\n\n   reponses: %s" % list(responses.keys()))
    if no_response:
        print("\n    no response received in time, even after retries: %s" % no_response)




#-------------------------------------------------------------------------------------------------------------------
#               Splits the IPs in the specified range in the group of 20
#               and calls send_ping function to send the ICMP ping
#-------------------------------------------------------------------------------------------------------------------

def discover(self):

    flag = True
    addr_current = self.addr_start
    print("hi")

    addrs = list()
    threads = []
    while self._match_addr(addr_current,self.addr_end) > 0:
        print("in\n")
        count = 0
        addrs = []
        while count<30 and self._match_addr(addr_current,self.addr_end)>=0:
            addrs.append(addr_current)
            addr_current = self._increment_addr(addr_current)
            count = count + 1

        print(addrs)
        #discover(addrs,2)
        try:
            t=threading.Thread(target= self._send_ping, args=(addrs,2, ) )
            threads.append(t)
            t.start()
        except:
            print ("Error: unable to start thread")






class NetworkDiscovery(object):
    def __init__(self,start ,end):
        self.addr_start = start
        self.addr_end = end

    _increment_addr = increment_addr
    _match_addr = match_addr
    _discover = discover
    _send_ping = send_ping






if __name__ == "__main__":

    net = NetworkDiscovery("172.16.1.1","172.16.1.210")
    net._discover()
