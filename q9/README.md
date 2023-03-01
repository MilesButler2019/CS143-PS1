# Instructions

Within the topo.py file it creates a network with topology and delays as the image below

<img width="792" alt="Screen Shot 2023-02-28 at 11 31 04 PM" src="https://user-images.githubusercontent.com/47306315/222045203-b2cb67eb-b542-40ff-ba90-c2c083c11483.png">


To run the dijkstra.py file

`cd ~/pox/pox/misc/`

`pox.py misc.dijkstra &`

`sudo mn --custom topo.py --topo custom --controller remote --mac --link tc`


How it works:

We first make a mapping of the hosts then we update the flow table on the switch to route the packets accordingly
