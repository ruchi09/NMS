#!/usr/bin/python3

import sqlite3
import threading
from multiping import multi_ping
import ctypes
import os
import sys
import logging


sem_db = threading.Semaphore()


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
#               Uses multiping module to send pings and store the recieved pings in
#-------------------------------------------------------------------------------------------------------------------

def send_ping(self,addrs,no_of_retries):

    logging.debug('Starting Ping')

    responses, no_response = multi_ping(addrs, timeout=1, retry=2,ignore_lookup_errors=True)
    print("\n\n\n\n   reponses: %s" % list(responses.keys()))
    if no_response:
        print("\n    no response received in time, even after retries: %s" % no_response)

    self.active_ips = self.active_ips | set(responses)

    logging.debug('Done Storing')




#-------------------------------------------------------------------------------------------------------------------
#               Splits the IPs in the specified range in the group of 20
#               and calls send_ping function to send the ICMP ping
#-------------------------------------------------------------------------------------------------------------------

def discover(self):

    flag = True
    addr_current = self.addr_start
    #print("hi")

    addrs = list()
    threads = []
    while self._match_addr(addr_current,self.addr_end) > 0:
        print("in\n")
        count = 0
        addrs = []
        while count<40 and self._match_addr(addr_current,self.addr_end)>=0:
            addrs.append(addr_current)
            addr_current = self._increment_addr(addr_current)
            count = count + 1

        print(addrs)
        # self._send_ping(addrs,2)
        #discover(addrs,2)
        try:
            t=threading.Thread(target= self._send_ping, args=(addrs,2, ) )
            threads.append(t)
            t.start()
            t.join()
        except:
            print ("Error: unable to start thread")


    # sem_db.acquire()
    conn = sqlite3.connect('NMS.db')
    c = conn.cursor()
    logging.debug('Starting storage')


    for ip in self.active_ips:
        print(ip)
        c.execute("INSERT INTO IPs VALUES (?)",(ip,))

    conn.commit()
    conn.close()
    # sem_db.release()
    print self.active_ips
    print("i am exiting discovery")







class NetworkDiscovery(object):

    active_ips = set()
    # Costructor
    def __init__(self,start ,end):
        self.addr_start = start
        self.addr_end = end
        # checking the admin privilages
        try:
         is_admin = os.getuid() == 0
        except AttributeError:
         is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

        if is_admin==False:
            print ("\n\n--------------------------------------------------------")
            print ("    Administrative Privilages Required!!!!")
            print ("--------------------------------------------------------\n\n")
            sys.exit()

        # preparing logs format
        logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] (%(threadName)-10s) %(message)s',)





    def assign_starting_address(self,start):
        self.addr_start = start

    def assign_ending_address(self,end):
        self.addr_end = end

    def create_da_and_table():

        conn = sqlite3.connect('NMS.db')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IPs (IP text)''')
        c.commit()
        conn.close()



    _increment_addr = increment_addr
    _match_addr = match_addr
    _discover = discover
    _send_ping = send_ping







if __name__ == "__main__":



    net = NetworkDiscovery("172.16.255.0","172.16.255.255")
    net._discover()
