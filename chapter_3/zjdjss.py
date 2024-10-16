import heapq
import networkx as nx
class Node:
    def __init__(self,state,parent=None,action=0) -> None:
        self.state=state #存储此节点对应的图顶点
        self.parent=parent #存储此节点对于的父节点
        self.action=action #存储父节点生成此节点产生的cost
        if self.parent==None:
            self.path_cost=0
        else:
            self.path_cost=self.parent.path_cost+self.action #存储初始整个路径的cost
class Frontiner:
    def __init__(self) -> None:
        self.heap=[]
    def add_node(self,node:Node):
        heapq.heappush(self.heap,(node.path_cost,node))
    def pop(self):
        return heapq.heappop(self.heap)[1]    
    def empty(self):
        if len(self.heap)==0:
            return 1
        else:
            return 0 
class Reached:
    def __init__(self) -> None:
        self.reached={}
    def add_state(self,node:Node):
        self.reached[node.state]=node
class Graph(nx.DiGraph):
    def __init__(self):
        self.graph=nx.DiGraph()
    def create_graph(self,graph:list[tuple]):
        self.graph.add_weighted_edges_from(graph)
        return self.graph
    
class Problem:
    def __init__(self,problem_initial_state,problem_goal_state,problem_graph:Graph) -> None:
        self.problem_initial_state=problem_initial_state
        self.problem_goal_state=problem_goal_state
        self.problem_graph=problem_graph
    def is_goal(self,node):
        if node.state==self.problem_goal_state:
            return 1
        else:
            return 0
def expand_node(problem:Problem,node:Node):
    s_parent=node.state
    for next_state in list(problem.problem_graph.graph.neighbors(s_parent)):
        yield Node(state=next_state,parent=node,action=problem.problem_graph.graph.edges[s_parent,next_state]['weight'])
        
def Best_First_Search(problem:Problem):
    node=Node(state=problem.problem_initial_state)
    frontier=Frontiner()
    frontier.add_node(node)
    reached=Reached()
    reached.add_state(node)
    while not frontier.empty():
        node=frontier.pop()
        if problem.is_goal(node):
            return node
        for child in expand_node(problem,node):
            s=child.state
            if s not in reached.reached.keys() or (child.path_cost<reached.reached[s].path_cost):
                reached.reached[s]=child
                frontier.add_node(child)
    print('没有找到最优解')
    return None
def get_path(problem:Problem,node:Node):
    result_path=[]
    path_cost=node.path_cost
    while node.state!=problem.problem_initial_state:
        result_path.append(node.state)
        node:Node=node.parent
    result_path.append(problem.problem_initial_state)
    return list(reversed(result_path)),path_cost
if __name__=="__main__":
    problem_graph = Graph()
    #graph=[(1,2,1),(2,3,3),(2,4,4),(3,5,3),(4,5,1),(5,6,2)]
    graph=[(1,2,2),(1,3,1),(2,4,4),(3,4,3),(4,5,5),(4,6,7),(5,7,8),(6,7,10)]
    problem_graph.create_graph(graph)
    problem=Problem(1,7,problem_graph)
    result_node=Best_First_Search(problem)
    print(get_path(problem,result_node))
    