#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Week 5 Assignment"""

import argparse
import csv
import urllib2


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="Enter a URL linking to a .csv file.")
parser.add_argument('-s', '--servers', help="Enter the number of servers.")
args = parser.parse_args()


def downloadData(url):
    """Opens a supplied URL link.

    Args:
        url(str): A string for a website URL.

    Returns:
        datafile(various): A variable linked to an applicable datafile found at
        the supplied URL, if valid.

    Example:
        >>> downloaddata('https://s3.amazonaws.com/cuny-is211-spring2015/requests.csv')
        <addinfourl at 3043697004L whose fp = <socket._fileobject object at
        0xb5682f6c>>

	===================
	OUTPUT OF PROGRAM:
	===================
        py_lover@DDOSER:~/Desktop/IS211 - Software App Prog II$ python simulation.py -u https://s3.amazonaws.com/cuny-is211-spring2015/requests.csv

        Average Wait 2502.00 secs 5006 tasks remaining.
    """
    datafile = urllib2.urlopen(url)
    return datafile


class Queue:
    """A Queue class.

    Stores data in a queue abstract data type.
    """
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Server(object):
    """A computer server class.

    Performs server functions passed from the simulateOneServer function.
    """
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_time()


class Request(object):
    """A Request class.

    Simulates requests to a server by using objects passed to it from the
    simulateOneServer function.
    """
    def __init__(self, req_sec, process_time):
        self.timestamp = req_sec
        self.process_time = process_time

    def get_stamp(self):
        return self.timestamp

    def get_time(self):
        return self.process_time

    def wait_time(self, current_time):
        return current_time - self.timestamp


def simulateOneServer(datafile):
    """Simulates a server by operating on a list of requests contained in a .csv
    file. The function operates over the file row by row, adding processing
    times into a queue based on how many seconds are left in the process.

    Args:
        datafile(obj): An object pointing to a .csv file downloaded from a
        supplied URL.

    Returns:
        (str): A string indicating the average wait time, and the size of the
        server queue when it reaches the end of the file.

    Example:
        >>> my_file=downloaddata('https://s3.amazonaws.com/cuny-is211-spring2015
        /requests.csv')
        >>> simulateOneServer(my_file)
        >>> 'Average Wait 250 sec 5400 tasks remaining.'
    """
    readfile = csv.reader(datafile)
    lab_server = Server()
    server_queue = Queue()
    waiting_times = []

    for line in readfile:
        req_sec = int(line[0])
        process_time = int(line[2])
        task = Request(req_sec, process_time)
        server_queue.enqueue(task)

        if (not lab_server.busy()) and (not server_queue.is_empty()):
            next_task = server_queue.dequeue()
            waiting_times.append(next_task.wait_time(req_sec))
            lab_server.start_next(next_task)

        lab_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print('Average Wait %6.2f secs %3d tasks remaining.'
          % (average_wait, server_queue.size()))


def simulateManyServers(datafile, servers):
    """A function to simulate a number of servers depending on the number
    passed from argparse.

    I did not figure out how to successfully create multiple servers to cycle
    each line of the file through and calculate the end result.
    """
    # servers =


def main():
    """Combines downloadData, processData, and displayPerson into one program to
    be run from the command line.
    """
    if not args.url:
        raise SystemExit
    try:
        datafile = downloadData(args.url)
    except urllib2.URLError:
        print 'Please enter a valid URL.'
        raise
    else:
        if not args.servers:
            simulateOneServer(datafile)
        else:
            simulateManyServers(datafile, args.servers)

if __name__ == '__main__':
    main()
