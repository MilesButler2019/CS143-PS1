#from copy import deepcopy
import csv
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr
from collections import namedtuple
from collections import defaultdict

log = core.getLogger()
delayFile = "delay.csv"

#List hosts and which switch they connect to
hosts = {'h13': 's12', 'h15': 's14', 'h17': 's16', 'h19': 's18'}

#Generate dictionary of nodes connected to links in csv
link_to_node = {"g": ("s11","s12") , "h": ("s12","s14"),
                "i": ("s14","s16"),"j": ("s16","s18"),"k": ("s11","s18"),
                "l": ("s12","s18"),"m": ("s12","s16"),"n": ("s14","s18")}

#generate mapping of connections
switch_ports = {'s11':{'s12': 1, 's18': 2}, 's12': {'h13': 1, 's11': 2, 's14': 3, 's18': 4, 's16': 5},
    'h13': {'s12': 0}, 's14': {'h15': 1, 's12': 2, 's16': 3, 's18': 4}, 'h15': {'s14': 0},
    's16': {'h17': 1, 's14': 2, 's18': 3, 's12': 4}, 'h17': {'s16': 0},'s18': {'h19': 1, 's16': 2, 's11': 3, 's12': 4, 's14': 5},
    'h19': {'s18': 0},
}

#Get connections from mininet
hostMappings = {
    'h13': ('10.0.0.1', '00:00:00:00:00:01'),
    'h15': ('10.0.0.2', '00:00:00:00:00:02'),
    'h17': ('10.0.0.3', '00:00:00:00:00:03'),
    'h19': ('10.0.0.4', '00:00:00:00:00:04'),
}

#Initiate dicts for storing values
delays = {}
switches = []
node_n = defaultdict(set)

#Open and store values from csv
with open(delayFile, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader)
    for link, delay in csvreader:
        s1, s2 = link_to_node[link]

        node_n[s1].add(s2)
        node_n[s2].add(s1)

        delays[(s1, s2)] = int(delay)
        delays[(s2, s1)] = int(delay)

        switches.append(s1)
        switches.append(s2)


class Dijkstra(EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Dijkstra Module")

    def _dijkstra(self, source):
        to_check = switches.copy()
        dist = defaultdict(lambda: float('inf'))
        dist[source] = 0
        prev = {}
        
        while to_check != []:
            minDist = float('inf')
            close = min(to_check, key=lambda x: dist[x])
            to_check.remove(close)

            for node in node_n[close]:
                alt = dist[close] + delays[(close, node)]
                if alt <= dist[node]:
                    dist[node] = alt
                    prev[node] = close
                    
        return dist, prev

    def _getPortMapping(self, source):
        dist, prev = self._dijkstra(source)
        ports = {}

        for dest_H, dest_S in hosts.items():

            if source == dest_S:
                ports[dest_H] = switch_ports[source][dest_H]
                continue

            while source != prev[dest_S]:
                dest_S = prev[dest_S]
            ports[dest_H] = switch_ports[source][dest_S]

        return ports

    def _handle_ConnectionUp(self, event):
        switch = 's' + str(event.dpid)
        ports = self._getPortMapping(switch)

        for host, (ip, mac) in hostMappings.iteritems():
            port = ports[host]
            msg_mac = of.ofp_flow_mod()
            msg_mac.match.dl_dst = EthAddr(mac)
            msg_mac.actions.append(of.ofp_action_output(port=port))
            event.connection.send(msg_mac)
            msg_ip = of.ofp_flow_mod()
            msg_ip.match.nw_dst = IPAddr(ip)
            msg_ip.match.dl_type = 2054
            msg_ip.actions.append(of.ofp_action_output(port=port))
            event.connection.send(msg_ip)

        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))



def launch():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)
