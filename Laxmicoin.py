#Creating a Cryptocurrency On Python And Testing It On Postman

'''
#To Be Installed -
Flask -  pip install Flask==0.12.2
Postman - https://www.getpostman.com/
requests==2.18.4 - pip install requests==2.18.4.

What makes a blockchain a cryptocurrency?
Transactions and Consensus Protocol
Transaction -
The principle of cryptocurrency is that we are able to exchange these cryptocurrencies through transactions 
that are added to new blocks which are mined by the miners in the most secure way. i.e once when some  
transactions are added to a new block the block is integrated to blockchain and then its impossible to modify
anything in the block.
Consensus protocol - 
The second pillar will be to build a consensus function to make sure that each node in the decentralized 
network has the same chain. Because once some new transactions are integrated to a new block which is added 
to the blockchain.
We need to make sure that all the nodes in the network get also their chain updated with this last mined block 
containing the transactions. And this particular check is called the consensus.

Changes made to blockchain.py to make it a cryptocurrency-
1 - Added more libraries
2 - Added transaction variable to __init__  method & the transaction key to the dictionary of create_block function
3 - Defining a new function to create a format for transaction i.e a format for sender, receiver, and the
amount of coins exchanged. This function ll also append the transaction to the list of transactions before they
are integrated to the block.
4 - Adding nodes variable to the __init__ method because we ll need nodes to consider consensus protocol else
there ll be no point for consensus protocol.
5 - Defining a new function add_node to add any node to set of the self.node=set() by taking the address of the 
nodes.
6 - Defining a new function for the consensus protocol replace_chain, it ll look into all the nodes in our 
decentralized network it ll check the chain of each of these nodes and ll spot the longest chain and if any 
of the nodes having shorter chains ll get replaced by the longest chain.
7 - Creating an address for the node on port 5000 and Modifications to Part II - Mining the Blockchain, these 
required modifications have to do with transactions we have to integrate the transaction to the response.
8 - Creating a POST request to add a transaction to the blockchain
9 - Decentralizing the blockchain, Creating a POST request to connect new nodes and creating a request to
replace the chain in any node that is not updated, that is it doesnt contain the last version of blockchain
right after a new block is mined on another one.
10 - Creating a GET request for 'replacing the chain if needed' to get boolean True or False using the 
.replace_chain function from part I on the blockchain to return response
11 - Creating the JSON files which ll be needed to post in the POSTMAN when we ll interact with the blockchain
to exchange the cryptocurrencies. 
Two JSON Files ll be created -
One Json file ll contain all the address of the nodes 
and the other JSON file ll contain the right format of the transactions with the right keys, i.e sender, receiver, amount.
12 - Creating 3 python files with this same code and just different ports for server -
This code is a general form of code for a cryptocurrency, To make it work on a decentralize network,
Creating 3 python files with this same general form of code and running it on 3 different ports.
User 'A' ll be connected to port 5001 'B' ll be connected to 5002 and 'C' ll be connected to 5003.
'''

#Getting Started

#Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request 
'''
From flask lbrary we are not just importing the flask class and jsonify file but also request module this 
time because we ll be connecting to some nodes and to connect to the nodes we need get json function and 
this function ll be taken from the request module.
'''
import requests
from uuid import uuid4 #UUID4 generate a random UUID for node_address
from urllib.parse import urlparse

#Part I - Building a Blockchain

class Blockchain:
    def __init__(self):
        self.chain=[]                                 
        self.transactions=[]
        self.nodes=set()    
        '''Nodes are not ordered because they are supposed to be all around the world And for also 
        computational purpose the nodes are initialized to an empty set instead of empty list. 
        https://stackoverflow.com/questions/1035008/what-is-the-difference-between-set-and-list
        '''
        '''
        Introducing a separate list which will contain the transactions before they are added to a block, 
        originally the transactions are not into a block they're added into a block as soon as a block is mine. 
        Once a block is mined all the transactions of the lists will get into a block and the list of 
        transactions will become empty. And this empty list will be reused to welcome some new transactions 
        that will be added to a new future block.
        '''
        self.create_block(proof=1, previous_hash='0')
    
    def create_block(self,proof,previous_hash):
        block={'index':len(self.chain)+1,
               'timestamp':str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':previous_hash,
               'transactions':self.transactions 
#The value of transactions key ll be self.transactions, we are taking self here because transaction is a variable of the class.
               }
        self.transactions=[]    
#After a block is created, lists will get into it and then self.transactions will become empty. And this empty list will be reused for new transactions.
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
        
    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof=True
            else:
                new_proof +=1
        return new_proof
              
    def hash(self,block):
        encoded_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index<len(chain):
           
            #1ST CHECK - previous hash of the current block is the hash of the previous block
            
            block=chain[block_index]
            if block['previous_hash']!=self.hash(previous_block):
                return False
            
            #2ND CHECK - Proof of each block is valid
            
            previous_proof=previous_block['proof']
            proof=block['proof']
            hash_operation=hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block = block
            block_index +=1
        return True
    
    def add_transaction(self,sender,receiver,amount): 
        '''Its a function to create a format for transaction i.e a format for sender,
        receiver, and the amount and appending the transaction to the list of transactions
        before they are integrated to the block.'''
        self.transactions.append({'sender':sender,
                                  'receiver':receiver,
                                  'amount':amount})
        previous_block=self.get_previous_block() 
        return previous_block['index']+1    
#The transactions are supposed to appened to the new future block, as soon as it ll be mined, so thats why current block + 1.
    
    def add_node(self,address): #function to add any node to the self.nodes=set() by taking address of the nodes
        parsed_url=urlparse(address) #parsed_url is a new variable that ll store the component of the url (address)
        '''
        #The URL parsing functions focus on splitting a URL string into its components.
        One of the function is .netloc
        What netloc does is that -
        Example https://www.googly.com/8892 the netloc component ll be 8892 or 
        http://127.0.0.1:5000/ the netloc component ll be 127.0.0.1:5000,
        thats what we want to add to the set. The address of the node and not the url.
        For more -
        https://www.saltycrane.com/blog/2008/09/python-urlparse-example/
        '''
        self.nodes.add(parsed_url.netloc) #Since its a set so we cant use append, instead we used add.
        
    def replace_chain(self):
        network=self.nodes #Its a variable containing all the nodes 
        longest_chain=None 
        '''Its a variable with the longest chain, We dont know yet which chain is the longest in the network 
        so initialized it to none. We ll make a for loop to scan the network to find the longest chain, and as 
        we get that the variable longest_chain ll be the longest chain of the network'''
        max_length=len(self.chain)
        '''
        In order to find the longest chain we ll simply compare the length of the chains of all the nodes in 
        the network and therefore on this same idea of introducing this longest chain variable which ll 
        become the largest chain at some point well we ll introduce the max length variable which ll be the 
        length of the largest chain.
        
        Its a variable with the length of the largest chain, its not initialized to zero or none, its 
        initialized with the chain we are currently dealing with i.e. self.chain. And if we find a chain
        with length larger than the self.chain, max_length variable ll be updated and accordingly we
        ll update the longest_chain variable
        '''
        for node in network:    
#Runninng a for loop to iterate on the nodes of the network, For each node in the network we ll get a response of the following request
            response=requests.get(f'http://{node}/get_chain')
            '''Finding the largest chain - 
            Previously when we built the blockchain, we defined a function, get_chain request that just not
            only return the whole chain but also the length of the chain.
            we ll put this request in the replace_chain method so we can get the length of all the blokchains 
            of all the nodes in the network, and by this way ll find the largest chain in the network.
            To make that request we ll use the get function from the requests library that ll get the 
            response exactly as response of get_chain request i.e the same data as response of get_chain.
            The argument that the requests.get function ll recieve is the address of the node(Generalise form), 
            Example - 
            Earlier when we were dealing with a single chain we used address of that node having that chain,
            that was http://127.0.0.1:5000/ (the nodes are differentiated by their ports, Different nodes has 
            this common url and then different port, every single port represent a different node) and now 
            when the system is decentralized there ll be an 'n' no. of nodes having 'n' no. of blockchains in
            the network, so instead of putting the url with the port of single node we have to generalize it 
            for any node in the loop so we ll replace it with 'node', we have put it in brackets because 
            we have used f string function.
            What is f string in python? https://www.youtube.com/watch?v=s6C3kYCNmLc'''
            if response.status_code==200: 
                '''get_chain request not only returns the response in json format, 
                but also check HTTP status code 200 to confirm everything is OK,
                so we need to do quick check here too. If everything is OK, then the length is taken.'''
                length=response.json()['length']
                '''Length is a variable having the length of the chain, The Response is given in json format 
                is exactly the dictonary format with keys and values. So we are taking the length key of a 
                dictionary which ll get the length of the chain. Now we have length of the chain so we can 
                check if it is the longest chain.
                '''
                chain=response.json()['chain']
                ''' But we also want to replace the chain if indeed this 'length' is not the largest one,
                therefore we ll also get the chain from response, in json format but with different key 
                i.e. chain, because get_chain request returns length as well as the chain'''
                if length>max_length and self.is_chain_valid(chain):
                    '''Now we ll check, If the length of the chain we just got in the response is larger than
                    the largest length which is in max length variable
                    and we also going to check the chain using 'is_chain_valid' method,
                    which ll check that the chain we just got in the response i.e the chain in our node is 
                    valid, we need to check this otherwise this chain has no reason to exist.
                    Since is_chain_valid is method of our class so we need to add self and taking 
                    an argument as chain
                    '''
                    '''
                    if length>max_length and the chain is valid, then we need to update max_length variable
                    because we found a length that is larger than the max length
                    and longest_chain which was initialised to none ll need to be updated as chain of the
                    response that indeed has a length larger than the maximum length. Basically its the
                    largest chain found in the loop over our nodes.
                    '''
                    max_length=length
                    longest_chain=chain
        if longest_chain: #If longest_chain is not none (The syntax is a python trick)
            ''''
            if the longest_chain is not none that is if the chain was replaced, well in that case we are 
            going to return True just to specify that the chain was replaced. and also we are going to 
            replace the chain because we actually havent done it yet. We have replaced the longest_chain 
            variable but our chain in the blockchain self here was not replaced yet effectively.
            '''
            self.chain=longest_chain
            return True
        return False 
    #If no replacement was made and therefore our chain is originally the longest chain then ll return false to specify it.
                    
#Part II - Mining the Blockchain
#Creating a Web App 
app = Flask(__name__)    #To Create Web App, Follow Flask Quickstart for in depth details.

#Creating an address for the node on port 5000
node_address=str(uuid4()).replace('-','') 
'''
Why do we need a node address?
Because whenever miner mines a new block, miner ll get some cryptocoins as their reward, therefore there is a
transaction - from the node to the miner. And that is why its fundamental to get an address for this node.
So whenever we mine a new block, there ll be a transaction from this node address to yourself. This is the
first type of transaction. Second type of transaction or general transactions are from someone to someone.
How do we get a node address?
UUID4 generates random UUID for the node address, We used replace function to replace '-' with nothing '',
because these UUID contains '-' between the numbers and converted the UUID into a string.
''' 
#Creating a Blockchain
blockchain=Blockchain() #Creating blockchain object for the Blockchain class.

#Mining a new block - 1st GET Request
@app.route('/mine_block',methods=['GET']) 
def mine_block():
        previous_block=blockchain.get_previous_block()
        previous_proof=previous_block['proof']
        proof=blockchain.proof_of_work(previous_proof)
        previous_hash=blockchain.hash(previous_block) 
        blockchain.add_transaction(sender=node_address,receiver='USER',amount=1) 
        '''***Adding transaction to 'blockchain' object of our 'Blockchain' class, To use add_transaction 
        method on our 'blockchain' object we simply need to add here .add_transaction. Now comes
        who ll be the receiver, sender and what ll be the amount? As explained miner ll be rewarded
        for mining a block. The sender ll be the node_address, the receiver ll be the miner and the amount
        is the reward for mining a block.
        '''
        block=blockchain.create_block(proof,previous_hash)
        response={'message':'Congrats, You just mined a block',
                  'index':block['index'],
                  'timestamp':block['timestamp'],
                  'proof':block['proof'],
                  'previous_hash':block['previous_hash'],
                  'transactions':block['transactions']} #Adding transaction key
        return jsonify(response), 200 

#Getting the full Blockchain - 2nd GET Request
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,
              'length':len(blockchain.chain)
              }
    return jsonify(response), 200

#Adding a new transaction to the Blockchain
'''
In order to add a transaction to the blockchain, we need to create a POST request.
In GET request we dont need to create anything to get a response but in POST request, to get a response 
we need to create something, that is why it is called POST request becuase we are posting something inside 
the HTTP client. In order to add a transaction to the blockchain, we need to post the transaction and to post
this transaction we ll create a JSON file which ll contain the keys of the transactions i.e sender, receiver,
amount of the coins exchanged. This information ll be posted to the JSON file and the response ll get the 
JSON file and this JSON file containing the transaction ll go through jsonify function and eventually this
transaction ll go into the next mined block
'''
@app.route('/add_transaction',methods=['POST'])
def add_transaction(): #Implementing a new request through a function, add_transaction
    json=request.get_json() #Getting the JSON file which was posted in the POSTMAN
    transaction_keys=['sender','receiver','amount'] 
    #Checking all the keys are present in the JSON file; transaction_keys is a variable having a list of sender, receiver and amount
    if not all (key in json for key in transaction_keys): 
        '''IF loop to check wether any of the key is not present in the transaction_keys
        variable, If something is missing return a missing message with HTTP status code
        for missing item or Bad request i.e 400''' 
        return 'Some elements of the transaction are missing',400
    '''If the transaction_keys have all keys, then we need to add the transaction to the next mined block.
    How to get the next mined block? We need to find the index of the next block, add_transaction method 
    returns the index of the next block that ll be mined, add_transaction method doesnt take the keys
    it takes the values of these keys, To get the values of the keys we need to take it from the json file,
    json file work same as python dictionaries, so in order to get the values of the transaction, we ll take
    the json variable which is exactly the json file containing the transaction.'''
    index=blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response={'message':f'This transaction ll be added to block {index}'} #response is a variable which ll contain the response 
    return jsonify(response), 201 #Returning the response with HTTP status code for success for POST Request, i.e 201

#Part III - Decentralizing the Blockchain

#Connnecting new nodes

'''why post request and not get?
Because basically we are going to create a new node in the decentralized network and therefore we are going to
register it. To register it we ll have a separate JSON file which ll contain all the node that we want in our
blockchain including the new one we want to connect and this JSON file ll be exactly what ll be posted in the
POSTMAN to make our post request
Whenever we want to connect to a new node to the blockchain, we ll simply need to add this node to the JSON
file that contains already the existing nodes and we ll post this JSON file using connect_node POST request
and this ll connect the new node to the network.'''
@app.route('/connect_node',methods=['POST'])
def connect_node():
    json=request.get_json() 
    '''Request to get for posting a new node in the network through the get json function which ll return this
    json file that ll contain all the nodes in the decentralized network'''
    
    nodes=json.get('nodes') 
    '''connecting new node to all other nodes in the network, To do that we ll simply use add_node function
    to add all the node of the JSON file to the blockchain network. But add_node takes an argument as address,
    but now the nodes are in JSON file so we cannot use directly the variable. So we ll use this get method,
    so this json.get ll get us exactly the value of this key, i.e the address contained in the list.
    This returns the values and to store these values we introduced nodes variable.
    '''
    if nodes is None: #Check for if nodes variable returns empty list
        return 'Error: No Nodes Found', 400
    for node in nodes: #Adding nodes one by one
        blockchain.add_node(node) #Taking the blockchain object and using add_node method which takes argument as address i.e nodes
    response={'Message': 'All the nodes are now connected. Thse Laxmicoin Blockchain now contains the following nodes:',
              'total_nodes': list(blockchain.nodes)} #Returning response as message with the list of total nodes in the network
    return jsonify(response), 201

#Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    '''
    We ll use a function which ll give us boolean true or false and on them we ll make a if and else condition
    which ll return two different messages
    To have this boolean we have a function replace_chain in Part - I which exactly returns True or False,
    This replace_chain function in Part - I does not simply change the chain by the longest one but also returns
    true or false, True if the chain is not the longest one and false if the chain is the longest one.
    '''
    is_chain_replaced=blockchain.replace_chain() 
    '''is_chain_replaced is a variable which ll have the boolean true or false, Using .replace_chain from
    Part - I on the blockchain ll return True or False''' 
    if is_chain_replaced:
        response = {'message': 'The nodes had different chain so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain} #returns the message and the blockchain
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200
    
#Running the app
app.run(host='0.0.0.0', port=5000)
