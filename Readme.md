# Creating a Cryptocurrency on Python and testing it on Postman

## To Be Installed -
Flask -  pip install Flask==0.12.2

Postman - https://www.getpostman.com/

requests==2.18.4 - pip install requests==2.18.4

### What makes a Blockchain a Cryptocurrency?
Transactions and Consensus Protocol.
1. Transaction -
The principle of cryptocurrency is that we are able to exchange these cryptocurrencies through transactions 
that are added to new blocks which are mined by the miners in the most secure way. i.e once when some  
transactions are added to a new block the block is integrated to blockchain and then its impossible to modify
anything in the block.
2. Consensus protocol - 
The second pillar will be to build a consensus function to make sure that each node in the decentralized 
network has the same chain. Because once some new transactions are integrated to a new block which is added 
to the blockchain.
We need to make sure that all the nodes in the network get also their chain updated with this last mined block 
containing the transactions. And this particular check is called the consensus.

### Changes that were made to the blockchain.py from the [Blockchain Repository](https://github.com/mdsalik7/Blockchain/blob/master/blockchain_with_inline_explaination.py) to make it a cryptocurrency -
1 - Added more libraries.  
2 - Added transaction variable to __init__  method & the transaction key to the dictionary of create_block function.  
3 - Defined a new function to create a format for transaction i.e a format for sender, receiver, and the
amount of coins exchanged. This function ll also append the transaction to the list of transactions before they
are integrated to the block.  
4 - Added nodes variable to the __init__ method because we ll need nodes to consider consensus protocol else
there ll be no point for consensus protocol.  
5 - Defined a new function add_node to add any node to the set of the self.node=set() by taking the address of the 
nodes.  
6 - Defined a new function for the consensus protocol replace_chain, it ll look into all the nodes in our 
decentralized network it ll check the chain of each of these nodes and ll spot the longest chain and if any 
of the nodes having shorter chains ll get replaced by the longest chain.  
7 - Created an address for the node on port 5000 and made modifications to Part II - Mining the Blockchain, these 
required modifications have to do with transactions we have to integrate the transaction to the response.  
8 - Created a POST request to add a transaction to the blockchain.  
9 - Decentralized the blockchain, Created a POST request to connect new nodes and created a request to
replace the chain in any of the node that is not updated, so that it doesnt contain the last version of blockchain
right after a new block is mined on another one.  
10 - Created a GET request for 'replacing the chain if needed' to get boolean True or False using the 
.replace_chain function from part I on the blockchain to return response.  
11 - Created the two JSON files which ll be needed to post in the POSTMAN when we ll interact with the blockchain
to exchange the cryptocurrencies.  
One Json file ll contain all the address of the nodes, 
and the other JSON file ll contain the right format of the transactions with the right keys, i.e sender, receiver, amount.  

## How To Execute -

This code is a generalised code for a cryptocurrency. To make it work on a decentralize network,
Create 3 python files with this same generalised code and just make it run on 3 different ports using 3 different kernels of python.
User 'A' ll be connected to port 5001, 'B' ll be connected to 5002 and 'C' ll be connected to 5003. To do it just find and replace 5000 with 5001 for A,
5002 for 'B' and 5003 for 'C'.    
But before executing, find and also replace, receiver='USER' in the all the 3 python files with receiver=A/B/C respectively.

#### Else  

Download all the Nodes from the repo and make it run on the different kernels of Python(Spyder).

### Interacting with the Crpytocurrency on Postman-

#### 1. Mining the genesis block on all the nodes 5001, 5002 and 5003.  
![ezgif com-gif-maker](https://user-images.githubusercontent.com/42892152/53284209-17b6c280-3777-11e9-841e-d6c17546e074.gif)  

#### 2. Connecting all nodes to each other i.e 5001 is connected to 5002 and 5003, 5002 is connected to 5001 and 5003, 5003 is connected to 5001 and 5002.  
![ezgif com-gif-maker 1](https://user-images.githubusercontent.com/42892152/53284381-8b59cf00-3779-11e9-8218-e9943cd3bef2.gif)  

#### 3. Miner 'A' on node 5001 mines a block.  
![screenshot 16](https://user-images.githubusercontent.com/42892152/53284423-569a4780-377a-11e9-9d0f-9fef6d96c060.jpg)  

#### 4. Getting the full blockchain.  
![screenshot 18](https://user-images.githubusercontent.com/42892152/53284459-f1932180-377a-11e9-999d-4ea02872e3b3.jpg)  

#### 5. Updating the blockchain on node 5002. Repeat it on node 5003 to update the blockchain on that node as well.    
![screenshot 19](https://user-images.githubusercontent.com/42892152/53284622-f2c54e00-377c-11e9-94fc-60c9dd3d1073.jpg)  

#### 6. Making a transaction of Laxmicoin from User A on node 5001 port to User B on node 5002.  
![screenshot 21](https://user-images.githubusercontent.com/42892152/53284652-74b57700-377d-11e9-8d30-c91a43767565.jpg)  

#### 7. Mining the block which ll contain the above transaction.  
![screenshot 22](https://user-images.githubusercontent.com/42892152/53284677-bb0ad600-377d-11e9-9b87-941274bfbb57.jpg)  

#### 8. Getting the updated blockchain with the latest mined block in it where the transaction is stored that was made between the two nodes above.  
![screenshot 23](https://user-images.githubusercontent.com/42892152/53284767-aa0e9480-377e-11e9-9c00-cbcf4a6c5350.jpg)  

#### 9. Updating the blockchain on node 5002. Repeat it on node 5003 to update the blockchain on that node as well.   
![screenshot 26](https://user-images.githubusercontent.com/42892152/53284886-19d14f00-3780-11e9-80d8-c90517f2e772.jpg)


