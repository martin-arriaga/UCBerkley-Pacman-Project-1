# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""


import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    "I got stuck here in DFS where I was able to pass all the tests except for the second one and so I uploaded my algorithm to ChatGPT"
    "and asked it if it spotted anything wrong with it"
    """
    This was the response: 
    Potential Issues or Points to Note:
    Redundant visited List:
    You're maintaining the visited list manually to avoid revisiting states. While this works fine in DFS, it's important to note that DFS can be inefficient in very deep or infinite search spaces. You may want to consider using a set for visited rather than a list for faster membership checking, as the in operator in lists is O(n) while it is O(1) for sets.
    Action List Update:
    When pushing a child state to the stack, the path (path_upto_child + [action]) is updated and passed along. This is fine for DFS, but if the state space is large, this may result in a lot of list copying. You might want to consider using an iterative approach or a generator in some cases.
    Returning the Path:
    When the goal is reached, you return the path (path_upto_child + [action]). Make sure that the function this code belongs to is returning the correct value at the right time (i.e., when the goal state is found).

    *** from this respones i was able to correct my algortihm, the main problem was that when i found my goal state i was sending path_upto_child + [action] and i should have just been returning path_upto_child***
    *** also i was checking if the child was a goal state and returning the path at the time, that meant that I never actually traveled to the child node. If one of the child node was a goal. i.e the second test, the alg would terminate early 
    I moved the problem.isGoal() to check the state when i pop the state, meaning i actually traveled to the node and the algorithm did not end prematurely.

    """

    fringe = util.Stack()
    list_of_paths_taken = []
    visited = set()
    fringe.push((problem.getStartState(), list_of_paths_taken))

    while not fringe.isEmpty():
        current_state, path_upto_child = fringe.pop()
        if current_state not in visited:
            visited.add(current_state)
            if problem.isGoalState(current_state):
                return path_upto_child
            neighbors = problem.getSuccessors(current_state)
            for child, action, cost in neighbors: #dfs does not need cost
                fringe.push((child, path_upto_child + [action]))

    #util.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    "Same algorithm as DFS but we use a different data structure, only thing that changes is the way we pop from the data structure."
    "instead of LIFO we use a queue that use FIFO"
    fringe = util.Queue()
    list_of_paths_taken = []
    visited = set()
    fringe.push((problem.getStartState(), list_of_paths_taken))

    while not fringe.isEmpty():
        current_state, path_upto_child = fringe.pop()
        if current_state not in visited:
            visited.add(current_state)
            if problem.isGoalState(current_state):
                return path_upto_child
            neighbors = problem.getSuccessors(current_state)
            for child, action, cost in neighbors:
                fringe.push((child, path_upto_child + [action]))
    #util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    list_of_paths_taken = []
    visited = set()
    cost = 0
    fringe.push((problem.getStartState(), list_of_paths_taken),cost)

    while not fringe.isEmpty():
        current_state, path_upto_child = fringe.pop()
        if current_state not in visited:
            visited.add(current_state)
            if problem.isGoalState(current_state):
                return path_upto_child
            neighbors = problem.getSuccessors(current_state)
            for child, action, cost in neighbors: # only thing that changes is that after we push to the fringe we update the priority
                current_cost = problem.getCostOfActions(path_upto_child + [action])
                #if current_cost >= cost :
                    #print("consistent")
                fringe.push((child, path_upto_child + [action]), current_cost)
                fringe.update((current_state, path_upto_child), current_cost) #from priority queue if state exist -> update position, does not exist -> push, state exist with same priority -> nothing
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    list_of_paths_taken = []
    visited = set()
    cost = 0
    fringe.push((problem.getStartState(), list_of_paths_taken), cost)

    while not fringe.isEmpty():
        current_state, path_upto_child = fringe.pop()
        if current_state not in visited:
            visited.add(current_state)
            if problem.isGoalState(current_state):
                return path_upto_child
            neighbors = problem.getSuccessors(current_state)
            for child, action, cost in neighbors:
                current_cost = problem.getCostOfActions(path_upto_child + [action]) + heuristic(child, problem) #used for priority
                #if current_cost >= cost + heuristic(child, problem):
                    #print("consistent")
                fringe.push((child, path_upto_child + [action]), current_cost)
                fringe.update((current_state, path_upto_child), current_cost )
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
