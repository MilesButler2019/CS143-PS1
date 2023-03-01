from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.util import dumpNodeConnections, irange
from mininet.link import TCLink

class Q9Topo(Topo):
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # Add switches
        s12 = self.addSwitch('s12')
        s14 = self.addSwitch('s14')
        s18 = self.addSwitch('s18')
        s16 = self.addSwitch('s16')
        s11 = self.addSwitch('s11')

        # Add hosts
        h13 = self.addHost('h13', delay='50ms', bw=10, max_queue_size=1000, use_htb=True)
        h15 = self.addHost('h15', delay='50ms', bw=10, max_queue_size=1000, use_htb=True)
        h17 = self.addHost('h17', delay='50ms', bw=10, max_queue_size=1000, use_htb=True)
        h19 = self.addHost('h19', delay='50ms', bw=10, max_queue_size=1000, use_htb=True)


        # Add links
        self.addLink(s12, s16, delay='100ms', link_name='link_m')
        self.addLink(s14, s18, delay='20ms',  link_name='link_n')
        self.addLink(s12, s14, delay='50ms',  link_name='link_h')
        self.addLink(s14, s16, delay='10ms',  link_name='link_l')
        self.addLink(s16, s18, delay='30ms',  link_name='link_j')
        self.addLink(s18, s12, delay='10ms',  link_name='link_l')
        self.addLink(s12, s11, delay='10ms',  link_name='link_g')
        self.addLink(s11, s18, delay='30ms',  link_name='link_k')

        # Add host-switch links
        self.addLink(s12, h13, bw=10, max_queue_size=1000, use_htb=True, link_name='link_s12_h13')
        self.addLink(s14, h15, bw=10, max_queue_size=1000, use_htb=True, link_name='link_s14_h15')
        self.addLink(s16, h17, bw=10, max_queue_size=1000, use_htb=True, link_name='link_s16_h17')
        self.addLink(s18, h19, bw=10, max_queue_size=1000, use_htb=True, link_name='link_s18_h19')

topos = {"custom": (lambda: Q9Topo())}
