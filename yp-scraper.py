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


#print   # body
#thrift-stores
#response1 = br.find_link(text_regex=r"pawn-shops", nr=1)
def t():
    data = g('http://www.yellowpages.com/lawrence-ks/thrift-stores')
    tree = etree.parse(StringIO(data),parser)
    #body/div/div/div/div/div/div/div/ul/li/a/div/div[3]/div[2]/div/span/span
    r= tree.getroot()   
#    for e in r.findall('.//div[@data-lid]'):

#    for e in r.findall('.//div[@class="info-business"]'):
#    for e in r.findall('.//div[@class="info-business-wrapper"]'):
    for e in r.findall('.//div[@class="clearfix result result-container track-listing vcard"]'):
        sid = e.get('data-lid')
        classn = e.get('class')
        #        if sid.find("data-lid")==0:
        #            print "===1---"
        print "SID:%s" % sid
        print "class:%s" % classn
        print(print2 (e))

# ATTRIB {'class': 'business-categories'}
# ATTRIB {'class': 'business-phone phone'}
# ATTRIB {'class': 'categories ellipsis'}
# ATTRIB {'class': 'city-state'}
# ATTRIB {'class': 'info-business'}
# ATTRIB {'class': 'info-business-additional'}
# ATTRIB {'class': 'info-business-wrapper'}
# ATTRIB {'class': 'listing-address adr'}
# ATTRIB {'class': 'locality'}
# ATTRIB {'class': 'postal-code'}
# ATTRIB {'class': 'region'}
# ATTRIB {'class': 'srp-business-name'}
# ATTRIB {'class': 'street-address'}
# ATTRIB {'class': 'what-where'}
# ATTRIB {'data-lid': '461709198', 'class': 'business-name fn org'}



#            print e.tostring()
            #print ElementTree.tostring(e)

t()
