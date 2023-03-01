# Instructions

Navigate to /home/mininet/pox

Run these two commands <br>
`sudo fuser -k 6633/tcp` <br>
`python pox.py forwarding.l2_learning misc.firewall & `

Open a new terminal window
`sudo mn --topo single,3 --controller remote --mac `


## How it works

Within the _handle_connectionUp_ method we first allow all traffic then iterate through the pairs of mac address that we want to block and update the flow table according to block these connections
