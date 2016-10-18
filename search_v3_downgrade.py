#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import xml.etree.ElementTree as ET


class CheckENV:

#    def __init__(self,name):
#        self.name = name

#    def CheckFile(self):
#        if os.path.exists(self.name):
#            print("processing " + self.name + " ...")
#        else:
#            print("Error! " + self.name + " DO NOT EXISTS, pleae check!")
#            sys.exit()

    def CheckFile(self,a):
        if os.path.exists(a):
            print("processing " + a + " ...")
        else:
            print("Error! " + a + " DO NOT EXISTS, pleae check!")
            sys.exit()

    def CheckDevice(self,a):
        print "Checking", a


    def CheckLocation(self,a):
        print "Checking", a


    def CheckComponent(self,a):
        print "Checking", a

class DownGrade:

    def __init__(self,device,location,component,action):
        self.device = device
        self.location = location
        self.component = component
        self.action = action

    def CheckPara(self):
        a = CheckENV()
        a.CheckDevice(self.device)
        a.CheckLocation(self.location)
        a.CheckComponent(self.component)

    def GetFile(self):
        scriptPath = os.getcwd()
        file = (scriptPath + "/" + self.device + "/" + self.location + "/nodes.xml")
        newfile = CheckENV()
        newfile.CheckFile(file)
        return file

    def GetIPlist(self):
        file = self.GetFile()
        tree = ET.parse(file)

        IPlist = []
#usage: node = tree.findall(".//*[@type='blender']/node")
        node = tree.findall(".//*[@type=\'%s\']/node" % self.component)
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
#        print iplist
        for ip in iplist:
            if (self.component == "blender"):
                print "blender component"
                url = 'http://%s:10080/Degradex' % ip
                print url

            elif (self.component == "smerger"):
                print ip,"smerger","13820"

            elif (self.component == "searcher"):
                print ip,"searcher","10103"

            elif (self.component == "dmerger"):
                print ip,"dmerger"

            elif (self.component == "list"):
                print "list"

            else:
                print "component wrong"

        print self.action,type(self.action)

if __name__ == '__main__':
    opt = DownGrade(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
#    opt.GetIPlist()
    opt.CheckPara()
    opt.ProcessCurl()
