# rdt
Simulation of a reliable data transfer protocol in an unreliable transmission network.
rdt_receiver is the server. Once connection is established, receives data from the sender.
Some data or acknowledgement packets might get corrupted or lost. This is handled by resending 
the data packet.

