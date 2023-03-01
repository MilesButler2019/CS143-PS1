#!/usr/bin/python
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.util import dumpNodeConnections, irange

class CustomTopo(Topo):
    """
    Simple Data Center Topology

    linkopts# - link parameters (where #: 1: core, 2: aggregation, 3: edge)
    fanout - number of child switches per parent switch
    """

    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        """Initialize topology and default options"""
        Topo.__init__(self, **opts)



        """ Implement your logic here """
       
        self.fanout = fanout

        self.host_count = 0
        self.edge_count = 0 
        
        # ADD Core SWITCH 
        core = self.addSwitch('c1')
        for i in range(1,self.fanout+1):
            agg = self.addSwitch('a{}'.format(i))
            #Add link from core to agg
            self.addLink(agg,core, bw=linkopts1['bw'], delay=linkopts1["delay"], loss=linkopts1['loss'],
            max_queue_size=linkopts1['max_queue_size'], use_htb=linkopts1["use_htb"])


            #Add Edge switches
            for i in range(1,self.fanout+1):
                self.edge_count += 1
                edge = self.addSwitch('e{}'.format(self.edge_count))
                self.addLink(agg, edge, bw=linkopts2['bw'], delay=linkopts2["delay"], loss=linkopts2['loss'],
                max_queue_size=linkopts2['max_queue_size'], use_htb=linkopts2["use_htb"])
                #Add hosts 
                for i in range(1,self.fanout+1):
                    host_count += 1
                    host = self.addHost("h%s" % host_count)
                    self.addLink(host, edge, bw=linkopts3['bw'], delay=linkopts3["delay"], loss=linkopts3['loss'],
                    max_queue_size=linkopts3['max_queue_size'], use_htb=linkopts3["use_htb"])


# topos = {"custom": (lambda: CustomTopo())}

## Uncomment below (or write your own code) to test your topology ##
linkopts1 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
linkopts2 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
linkopts3 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
# topos = { "custom": ( lambda: CustomTopo(linkopts1,linkopts2,linkopts3) ) }


def perfTest():
    "Create network and run simple performance test"
    topo = CustomTopo(linkopts1,linkopts2,linkopts3)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Testing bandwidth between h1 and h4")
    h1, h4 = net.get("h1", "h4")
    net.iperf((h1, h4))
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    perfTest()