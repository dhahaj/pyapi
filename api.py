"""
Python Mining API Interface
 - set parameters in the api.conf file
"""

import ConfigParser, time
import subprocess, os, mytools
from time import *
from mytools import *
from pycgminer import *
from pprint import *


cmds = ['config','summary','gpuenable','gpudisable','checkcmd','pools',
        'devs','gpu','gpucount','switchpool','enablepool','addpool',
        'poolpriority','poolqouta','disablepool','removepool','gpurestart',
        'gpuintensity','gpumem','gpuengine','gpufan','gpuvddc','quit',
        'notify','privileged','devdetails','restart','stats','check',
        'failover-only','setconfig','coin','debug']

cg = CgminerAPI()
global _pools

def cmd(c,a=None):
    req = cg.command(c,a)
    try: return req[c.upper()]
    except: return req
def scmd(c,a=None):
    pprint(cmd(c,a))
def disable(which):
    scmd('gpudisable',str(which))
def enable(which):
    scmd('gpuenable',str(which))
def stats():
    scmd('stats')
def sint(which,intensity):
    c = str(which) + ',' + str(intensity)
    scmd('gpuintensity',c)
def pools(simple=False):
    if not simple: scmd('pools')
    else:
        req = cmd('pools')
        ret = []
        print '\nPools:'
        for i in range(len(req)):
            pool = req[i]
            active = pool['Status']
            url = pool['URL']
            user = pool['User']
            num = pool['POOL']
            v = 'POOL %i, Status=%s, URL:%s, User:%s' % (num,active,url,user)
            print '\t',v
def rpool(which):
    scmd('removepool',str(which))
def apool(url,user,pswd):
    scmd('addpool',url+','+user+','+pswd)
def spool(which):
    scmd('switchpool',str(which))
def dpool(which):
    scmd('disablepool',str(which))
def fan(which,val):
    scmd('gpufan',str(which)+','+str(val))
def temp(which):
    #c = cmd('gpu',str(which))
    c = cg.gpu(str(which))['GPU']
    try: return c[which]['Temperature']
    except: return c
def clock(which,val=0):
    if val > 0: scmd('gpuengine',str(which)+','+str(val))
    else:
        c=cmd('gpu',str(which))
        try: return c[which]['GPU Clock']
        except: return c
def stop():
    try: cg.quit() #scmd('quit')
    except: print 'Cgminer Stopped'
def start(path=None, args=None):
    if path is None: path = ldcfg(item='path')
    if args is None: args = ldcfg(item='args')
    subprocess.call('CMD /C "start %s %s"' % (path, args))
    print 'Cgminer starting...'
    time.sleep(9)
    _pools = cmd('pools')
def ldcfg(item=None, name='api.conf', section='API'):
    config = ConfigParser.RawConfigParser()
    config.read(os.path.abspath(name))
    if item is not None:
        if config.has_option(section, item): return config.get(section, item)
        else: return ''
    return config
def get_time(sec=0,str=None):
    return time.ctime(sec)
    #t = time.gmtime(sec)
    #return time.asctime(t)

#os.spawnl(os.P_NOWAIT, 
