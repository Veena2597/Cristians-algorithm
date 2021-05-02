# Cristians-algorithm
A simplified distributed blockchain, where the local copies of the blockchain are consistent using clock synchronization, which is implemented using Cristian’s algorithm. There are 3 client and one clock servers.

The client clocks are simulated to drift by a small amount δ.
1. Every client saves a copy of the blockchain locally. Each block in the blockchain has a single transfer transaction.
2. There is an upper bound τ for the delivery time of each message sent in the network.
3. The clocks of all the clients are synchronized (using Cristian’s Algorithm) with a maximum discrepancy of δ.
