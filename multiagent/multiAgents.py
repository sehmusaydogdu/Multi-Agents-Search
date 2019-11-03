# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util,math,sys

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # baseScores represent [Food, Capsule, Ghost]
        baseScores = [1, 10, -20]
        resultScore = 0.0

        resultScore += currentGameState.hasFood(newPos[0], newPos[1]) + baseScores[0]
        foodList = successorGameState.getFood().asList()

        for food in foodList:
           resultScore -= baseScores[0] + (1 - math.exp(-1 * manhattanDistance(newPos, food)))

        currentGhostPosition = currentGameState.getGhostState(1).getPosition()
        newGhostPosition = successorGameState.getGhostState(1).getPosition()

        if newPos in [currentGhostPosition, newGhostPosition]:
            resultScore += baseScores[2]
        else:
            resultScore += baseScores[2] * math.exp(-1  * manhattanDistance(newPos, newGhostPosition))

        return resultScore

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.MinimaxSearch(gameState, 1, 0)

    #Min-Max Search Algorithm
    def MinimaxSearch(self, gameState, currentDepth, agentIndice):
        if gameState.isWin() or gameState.isLose() or currentDepth > self.depth:
            return self.evaluationFunction(gameState)

        legalActionList = gameState.getLegalActions(agentIndice)
        legalActionMoves =[]
        for legalAction in legalActionList:
            if legalAction != Directions.STOP:
                legalActionMoves.append(legalAction)

        nextStatus = agentIndice + 1
        nextDepth = currentDepth
        if nextStatus >= gameState.getNumAgents():
            nextStatus = 0
            nextDepth += 1

        results = []
        for actionMovies in legalActionMoves:
            generate = gameState.generateSuccessor(agentIndice, actionMovies)
            minimunSearchResult = self.MinimaxSearch(generate,nextDepth, nextStatus)
            results.append(minimunSearchResult)

        maxMovieValue = max(results)
        if agentIndice == 0 and currentDepth == 1:
            solution = []
            for i in range(len(results)):
                if results[i] == maxMovieValue:
                    solution.append(i)
            return legalActionMoves[solution[0]]

        if agentIndice == 0:
            return maxMovieValue
        return min(results)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def maximize(self, gameState, depth, numGhosts, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        maxValue = sys.maxsize * (-1)
        actionDirection = Directions.STOP

        for direction in gameState.getLegalActions(0):
          successor = gameState.generateSuccessor(0, direction)
          temp = self.minimize(successor, depth, 1, numGhosts, alpha, beta)
          if temp > maxValue:
            maxValue = temp
            actionDirection = direction
          if maxValue > beta:
              return maxValue
          alpha = max(alpha, maxValue)
        if depth > 1:
          return maxValue
        return actionDirection

    def minimize(self, gameState, depth, agentIndice, numGhosts, alpha, beta):
        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)

        minValue = sys.maxsize
        for direction in gameState.getLegalActions(agentIndice):
          successor = gameState.generateSuccessor(agentIndice, direction)
          if agentIndice == numGhosts:
            if depth < self.depth: tempVal = self.maximize(successor, depth + 1, numGhosts, alpha, beta)
            else: tempVal = self.evaluationFunction(successor)
          else:
            tempVal = self.minimize(successor, depth, agentIndice + 1, numGhosts, alpha, beta)
          if tempVal < minValue: minValue = tempVal
          if minValue < alpha: return minValue
          beta = min(beta, minValue)
        return minValue

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        min = sys.maxsize * (-1)
        max = sys.maxsize
        numAgent = gameState.getNumAgents() - 1
        return self.maximize(gameState, 1, numAgent , min, max)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def maxNode(self, gameState, numGhosts, counter):
        if gameState.isWin() or gameState.isLose() or counter == 0:
            return self.evaluationFunction(gameState)

        evaluations = []
        for action in gameState.getLegalActions():
            evaluations.append(self.minNode(gameState.generateSuccessor(self.index, action), numGhosts, counter))
        return max(evaluations)

    def minNode(self, gameState, numGhosts, counter):
        if gameState.isWin() or gameState.isLose() or counter == 0:
            return self.evaluationFunction(gameState)

        totalNumGhosts = gameState.getNumAgents() - 1
        currentGhostIndex = totalNumGhosts - numGhosts + 1
        legalActions = gameState.getLegalActions(currentGhostIndex)
        total = 0.0
        if numGhosts > 1:
            for action in legalActions:
                total += float(self.minNode(gameState.generateSuccessor(currentGhostIndex, action), numGhosts - 1, counter))
        else:
            for action in legalActions:
                total += float(self.maxNode(gameState.generateSuccessor(currentGhostIndex, action), totalNumGhosts, counter - 1))
        return total / (len(legalActions))

    def getAction(self, gameState):
        """
            Returns the expectimax action using self.depth and self.evaluationFunction
            All ghosts should be modeled as choosing uniformly at random from their
            legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = []
        evaluations = []

        for action in gameState.getLegalActions():
            actions.append(action)
            numGhosts = gameState.getNumAgents() - 1
            evaluations.append(self.minNode(gameState.generateSuccessor(self.index, action), numGhosts, self.depth))

        maxEvalIndex = evaluations.index(max(evaluations))
        return actions[maxEvalIndex]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    ghostStates = currentGameState.getGhostStates()
    pacmanPosition = currentGameState.getPacmanPosition()
    foodCount = currentGameState.getNumFood()
    currentScore = currentGameState.getScore()

    foodList = currentGameState.getFood().asList()
    foodPositionList = sorted(foodList, key=lambda pos: manhattanDistance(pacmanPosition, pos))

    bestFoodDist = 0
    if len(foodPositionList) > 0:
        bestFoodDist = manhattanDistance(foodPositionList[0], pacmanPosition)

    ghostEval = 0
    bestGhostDistance = sys.maxsize
    for ghost in ghostStates:
        distance = manhattanDistance(pacmanPosition, ghost.getPosition())
        if distance < bestGhostDistance:
            bestGhostDistance = distance
        if ghost.scaredTimer > distance:
            ghostEval += 200 - distance

    currentScore = currentScore -  foodCount + ghostEval + bestGhostDistance - 2 * bestFoodDist
    return currentScore

# Abbreviation
better = betterEvaluationFunction
