import parser

leduc = Game()
leduc.read_efg("leduc_tree.txt") #stores the extensive form game tree of leduc

class TeamBeliefDag:
    def __init__(self, game, team_players):
        self.game = game
        self.team_players = team_players
        self.active_nodes = []
        self.inactive_nodes = []
        self.child_of = {} # map from node, action : child node
        self.parent_of = {} # map from node : parent node


    def efg_to_tbdag(game, team_players):
        """
        Converts the extensive form in leduc to its equivalent team belief representation for team {team_players[0], team_players[1]} 
        """

        pass

class DagRegMin:

    def __init__(self, dag):
        self.dag = dag # tbdag representation of game
        self.regret = {} # map from active nodes s : {action (at s) : regret}
        self.x = {}
        self.x_prime = {} # unscaled probabilities

    def next_strategy(self):
        for node in self.dag.nodes:
            self.x[node], self.x_prime[node] = {}, {}
            for action in self.dag.child_of[node]:
                self.x[node] = 1
                self.x_prime[node][action] = 1
        
        for node in self.dag.active_nodes:
            if node != self.dag.root:
                self.x[node] = sum(self.x[parent] for parent in self.dag.parent_of[node])

            S = sum(max(self.regret[node][action], 0) for action in self.dag.child_of[node])

            for action in self.dag.child_of[node]:
                if S == 0:
                    self.x_prime[node][action] = 1 / len(self.dag.child_of[node])

                else:
                    self.x_prime[node][action] = max(self.regret[node][action] - S, 0) / S

                self.x[(node, action)] = self.x_prime[node][action] * self.x[node]
                

        return self.x

    def observe_utility(self, gradient):
        u = {}
        for node in self.dag.nodes:
            if node.node_type != "terminal":
                u[node] = 0

        for node in self.dag.active_nodes:
            u[node] += sum(u[(node,action)] * self.x_prime[(node,action)] for action in self.dag.child_of[node])
            for action in self.dag.child_of[node]:
                self.regret[node][action] += u[node] - u[(node,action)]

            for parent in self.dag.parent_of[node]:
                u[parent] += u[node]

    

            

