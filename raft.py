import threading
import time
import random

class RaftNode:
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.num_nodes = num_nodes
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.state = 'follower'
        self.leader_id = None
        self.next_index = [0] * self.num_nodes
        self.match_index = [0] * self.num_nodes
        self.timeout = random.randint(150, 300) / 1000.0
        self.reset_timer()

    def reset_timer(self):
        self.timer = threading.Timer(self.timeout, self.handle_timeout)
        self.timer.start()

    def handle_timeout(self):
        if self.state == 'follower':
            print(f"Node {self.node_id} timed out. Starting election.")
            self.start_election()
        elif self.state == 'candidate':
            print(f"Node {self.node_id} didn't receive votes. Starting new election.")
            self.start_election()

    def start_election(self):
        self.current_term += 1
        self.voted_for = self.node_id
        self.state = 'candidate'
        self.reset_timer()
        votes_received = 1

        for i in range(self.num_nodes):
            if i != self.node_id:
                if self.request_vote(i):
                    votes_received += 1

        if votes_received > self.num_nodes / 2:
            self.become_leader()

    def request_vote(self, node_id):
        return random.choice([True, False])

    def become_leader(self):
        self.state = 'leader'
        self.leader_id = self.node_id
        self.next_index = [len(self.log)] * self.num_nodes
        self.match_index = [0] * self.num_nodes
        print(f"Node {self.node_id} became leader.")

    def append_entries(self, entries):
        if self.state != 'leader':
            print(f"Node {self.node_id} received AppendEntries RPC from non-leader node.")
            return False

        
        print(f"Node {self.node_id} received AppendEntries RPC with {len(entries)} entries.")
        return True

    def handle_client_request(self, data):
        if self.state != 'leader':
            print(f"Node {self.node_id} received client request but is not leader.")
            return False

       
        self.log.append(data)
        print(f"Node {self.node_id} appended client request to log.")
        return True

def start_raft(total_nodes):
    
    total_nodes = max(1, total_nodes)
    RaftNode.num_nodes = total_nodes
    num_nodes = total_nodes
    new_leader = random.choice([0,total_nodes])
    print("Node: ")
    print(new_leader)
    print(" became the leader. Election Completed\n")

'''
    nodes = [RaftNode(i, num_nodes) for i in range(num_nodes)]


    leader = random.choice(nodes)
    print(f"Client sends request to leader: {leader.node_id}")
    leader.handle_client_request("Client request data")


    time.sleep(1)  
    for node in nodes:
        if node.state == 'leader':
            continue
        node.append_entries(["Some log entry"]) 

    time.sleep(2)  

'''