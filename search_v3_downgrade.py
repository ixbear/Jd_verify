#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import xml.etree.ElementTree as ET
import xml.dom.minidom

class CheckENV:

#    def __init__(self,name):
#        self.name = name

#    def CheckFile(self):
#        if os.path.exists(self.name):
#            print("processing " + self.name + " ...")
#        else:
#            print("Error! " + self.name + " DO NOT EXISTS, pleae check!")
#            sys.exit()

    def EchoUsage(self):
        a = """
        Usage: ./search_v3_downgrade.py [app|pc|staging_pc] [lf|mjq|staging] [blender|smerger|searcher|dmerger|clustermap] action
        Example: ./search_v3_downgrade.py app lf blender action
            """ 
        print a

    def CheckFile(self,a):
        if os.path.exists(a):
            print("processing " + a + " ...")
        else:
            print("Error! " + a + " DO NOT EXISTS, pleae check!")
            self.EchoUsage()
            sys.exit()

#    def CheckDevice(self,a):
#        print "Checking", a
#        if (a != "app" and a != "pc" and a != "mobile"):
#            print("Error! Device " + a + " DO NOT EXISTS, pleae check!")
#            self.EchoUsage()
#            sys.exit()
#    def CheckLocation(self,a):
#        print "Checking", a
#        if (a != "lf" and a != "LF" and a != "mjq" and a != "MJQ" and a != "staging"):
#            print("Error! Location " + a + " DO NOT EXISTS, pleae check!")
#            self.EchoUsage()
#            sys.exit()
#    def CheckComponent(self,a):
#        print "Checking", a
#        if (a != "blender" and a != "smerger" and a != "searcher" and a != "dmerger" and a != "clustermap"):
#            print("Error! Component " + a + " DO NOT EXISTS, pleae check!")
#            self.EchoUsage()
#            sys.exit()

class DownGrade:

    def __init__(self,device,location,component,action):
        self.device = device
        self.location = location
        self.component = component
        self.action = action

    def GetFile(self):
        scriptPath = os.getcwd()
        file = (scriptPath + "/" + self.device + "/" + self.location + "/nodes.xml")
        newfile = CheckENV()

#       no need to check device(app|pc) and location(lf|mjq), because if it's  error, this file will not exists.
        newfile.CheckFile(file)
        return file

    def GetIPlist(self):
        file = self.GetFile()
        tree = ET.parse(file)

        IPlist = []

#For Python2.7:
##usage:node = tree.findall(".//*[@type='blender']/node")
#       node = tree.findall(".//*[@type=\'%s\']/node" % self.component)
#        print "node is ", node
#        for IPall in node:
#            IPdict = IPall.attrib    #get a dict format
#            IPlist.append(IPdict["ip"])


#or For Python2.7:
#        for elem in tree.iterfind('clusters/cluster[@type="smerger"]/node'):
#                a = elem.attrib.get('ip')    #get a ip, str type
#                IPlist.append(a)

#For Python2.6
        dom = xml.dom.minidom.parse(file)
        root = dom.documentElement
        nodelist = root.getElementsByTagName('cluster') #get a nodelist object
        for i in nodelist:
            if ( self.component == i.getAttribute('type')):
                thelist = i.getElementsByTagName('node')
                for k in thelist:
                    IPlist.append(k.getAttribute('ip'))
        return IPlist

    def HTTPreq(self,url):
        print("Requsting: " + url)
        try:
            s = urllib2.urlopen(url).read()
#            print s
        except urllib2.HTTPError,e:
#            print e.code
            s = ("HTTPError! " + e.code)
#            sys.exit()
        except urllib2.URLError,e:
#            print str(e)
            s = ("URLError! " + str(e))
#            sys.exit()
        print s
#        return s

    def ProcessCurl(self):
        iplist = self.GetIPlist()
#        print iplist
        for ip in iplist:
            if (self.component == "blender"):
                print "blender component"
                url = 'http://%s:10080/Degradex' % ip
                self.HTTPreq(url)

            elif (self.component == "smerger"):
                url = 'http://%s:13820/%s' % (ip, self.action)
                self.HTTPreq(url)

            elif (self.component == "searcher"):
                url = 'http://%s:10080/Searcher' % ip
                self.HTTPreq(url)

            elif (self.component == "dmerger"):
                url = 'http://%s:10080/dmerger' % ip
                self.HTTPreq(url)

            elif (self.component == "list"):
                url = 'http://%s:10080/list' % ip
                self.HTTPreq(url)

            else:
                print "component wrong"

if __name__ == '__main__':
    if (len(sys.argv) != 5):
        print "Error! bad parameter!"
        a = CheckENV()
        a.EchoUsage()
    else:
        opt = DownGrade(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
#        opt.CheckPara()
        opt.ProcessCurl()
