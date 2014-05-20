import re
import mechanize
from lxml import etree
from StringIO import StringIO
from elementtree.ElementTree import ElementTree

import shelve

br = mechanize.Browser()
parser = etree.HTMLParser()
s = shelve.open("shelve")

def g(u):
    if u in s:
        return s[u]
    response1 = br.open(u)
    #    print br.title()
    #    print response1.geturl()
    #    print response1.info()  # headers
    #    for link in br.links():
    #        print (link.url)
    data = response1.read()
    s[u]= data
    return data

def print2(x,i=0):
    d = {
        'c' :[]
    }

    indent = "**" * i 
    classn = x.get('class') 
    href = x.get('href') 
    
    if x.text:
        t = x.text
        t= t.replace("\n","")
        #print "%s TEXT:%s=%s" % (indent,classn, t)
        d[classn]=t

    if href:
        d["href"]=href

#    if x.tail:
#        print "%s TAIL %s" % (indent,x.tail)

 #   print "%s ATTRIB %s" % (indent,x.attrib)

    for c in x:
        #print "%s ===%d---" % (indent,i)
        d["c"].append(print2(c,i=i+1))

    return d


def page(url):
    data = g(url)
#    print data
    string = StringIO(data)
    tree = etree.parse(string,parser)
    r= tree.getroot()   
    for f in r.findall('.//span'):        
        t = f.text
        if (t):
            print t.encode("ascii","replace")

    for f in r.findall('.//a'):        
        #print f
        h = f.get('href') 
        #print h

seen={}

#response1 = br.find_link(text_regex=r"pawn-shops", nr=1)
def t(url):
    #url like 'http://www.yellowpages.com/lawrence-ks/thrift-stores'
    if url.find('gallery?lid=')> 0:
        return
    print "going to get %s" % url
    data = g(url)
    tree = etree.parse(StringIO(data),parser)
    #body/div/div/div/div/div/div/div/ul/li/a/div/div[3]/div[2]/div/span/span
    r= tree.getroot()   
#    for e in r.findall('.//div[@data-lid]'):

    for f in r.findall('.//a'):        
        h = f.get('href') 
        if h:
            if h not in seen:
                if h.find("/lawrence") ==0:
                    print h
                    seen[h]=1
                    t("http://www.yellowpages.com" + h)
                #page(h)

#    for e in r.findall('.//div[@class="info-business"]'):
#    for e in r.findall('.//div[@class="info-business-wrapper"]'):
    for e in r.findall('.//div[@class="clearfix result result-container track-listing vcard"]'):
        sid = e.get('data-lid')
        classn = e.get('class')
        #        if sid.find("data-lid")==0:
        #            print "===1---"
        #print "SID:%s" % sid
        #print "class:%s" % classn
        #print(print2 (e))

        for f in e.findall('.//a'):        
            h = f.get('href') 
            if h.find("lid") > 0:
                if h.find(sid) > 0:
                    if h.find("http") == 0:
                        if h not in seen:
                            print h
                            seen[h]=1
                            page(h)


#t()

def cats():
    seen={}
    data = g('http://www.yellowpages.com/lawrence-ks')
    tree = etree.parse(StringIO(data),parser)
    r= tree.getroot()   
    for e in r.findall('.//a[@href]'):
        h = e.get('href') 
        if h.find("/lawrence-ks/") ==0:
            if h not in seen:
                seen[h]=1
                t("http://www.yellowpages.com" + h)

cats()
