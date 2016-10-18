#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import xml.etree.ElementTree as ET


class CheckENV:

    def __init__(self,name):
        self.name = name

    def CheckFile(self):
        if os.path.exists(self.name):
            print("processing " + self.name + " ...")
        else:
            print(self.name + " DO NOT EXISTS, pleae check!")
            sys.exit()

class DownGrade:

    def __init__(self,device,location,component,action):
        self.device = device
        self.location = location
        self.component = component
        self.action = action

    def GetFile(self):
        pyPath = os.getcwd()
        file = (pyPath + "/" + self.device + "/" + self.location + "/nodes.xml")
        newfile = CheckENV(file)
        newfile.CheckFile()
        return file

    def GetIPlist(self):
        file = self.GetFile()
        tree = ET.parse(file)

        IPlist = []
        node = tree.findall(".//*[@type='blender']/node")
        for IPall in node:
            IPdict = IPall.attrib    #get a dict format
            IPlist.append(IPdict["ip"])
#        print IPlist
        return IPlist

    def HTTPreq(url):
        try:
            s = urllib2.urlopen(url).read()
        except urllib2.HTTPError,e:
            print e.code
            sys.exit()
        except urllib2.URLErrror,e:
            print str(e)
            sys.exit()
        return s

    def ProcessCurl(self):
        iplist = self.GetIPlist()
        print iplist

        if (self.action == "blender"):
            url = http://10.191.5

        elif (self.action == "merger"):
            print "merger"

        elif (self.action == "searcher"):
            print "searcher"

        elif (self.action == "list"):
            print "list"

        else:
            print "action wrong"

if __name__ == '__main__':
    opt = DownGrade(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
#    opt.GetIPlist()
    opt.ProcessCurl()
