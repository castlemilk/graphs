import random
import math
import copy

def getColor(color):
  d = {
    'r': '\033[1;31;40m',
    'b': '\033[1;34;40m',
    'g': '\033[1;32;40m',
    'y': '\033[1;36;40m', #\u001b[33m
    '':  '\033[1;30;40m'
  }
  return d[color]
def getSegments(n, k, colors):
  """
  determine segments given values n total values and k distinct segments
  n - total values (height * width), the space we have to fill in the graph
  k - number of distinct segments to create
  colors - available colors to paint segments
  """
  permutations = []
  getSegmentsHelper([i for i in range(1, k+1)], [], permutations)
  return permutations

def getSegmentsHelper(array, currentPermutation, permutations):
  if not len(array) and len(currentPermutation):
    permutations.append(currentPermutation)
  for i in range(len(array)):
    newArray = array[:i] + array[i+1:]
    newPermutation = currentPermutation + [array[i]]
    getSegmentsHelper(newArray, newPermutation, permutations)

def getCombinations(n):
  array = [0] * n
  combinations = []
  getCombinationsHelper(combinations, array, 0, n, n)
  return list(filter(lambda x: len(x) == ((n / (math.sqrt(n)))), combinations))

def getCombinationsHelper(combinations, array, index, num, reducedNum):
  """
  find all combinations of numbers to reach num
  """
  if reducedNum < 0:
    return
  if reducedNum == 0:
    combo = []
    for i in range(index):
      combo.append(array[i])
    combinations.append(combo)
    return
  prev = 1 if index ==0 else array[index-1]
  for k in range(prev, num+1):
    array[index] = k
    getCombinationsHelper(combinations, array, index+1, num, reducedNum-k)

def printGraph(height, width, colors):
  choices = getCombinations(height * width)
  
  for attempt in range(100):
    visited = [[False for col in range(width)] for row in range(height)]
    graph = [['' for col in range(width)] for row in range(height)]
    segments = random.choice(choices)
    segments.sort(reverse=True)
    start_j = random.randint(0, width-1) # col
    start_i = random.choice([0, height-1]) if start_j > 0 and start_j < width else random.randint(0, height-1) # row
    start = [start_i, start_j]
    graph, err = paintGraph(graph, visited, start, segments, colors) 
    if err:
      print("graph invalid at attempt {} for {}".format(attempt, segments))
      break
    for i in range(height):
      for j in range(width):
        print("{}x{}".format(getColor(graph[i][j]), getColor(graph[i][j])), end="")
      print("")
    print("---")
  for i in range(height):
    for j in range(width):
      print("{}x{}".format(getColor(graph[i][j]), getColor(graph[i][j])), end="")
    print("")

def paintGraph(graph, visited, start, segments, colors):
  """
  create graph
  """
  
  if len(segments) != len(colors):
    raise Exception("need unique color for each segment")
  # print("segments: {}".format(segments))
  
  nextNodes = []
  for i in range(len(segments)):
    segment = segments[i]
    nextSegment = sum(segments[i+1:]) if i < len(segments) - 1 else 0
    if len(nextNodes):
    # two edges cases:
    # 1. check if next starting point has sufficient space for the next segment
    # 2. may be solved by 1. but need to have visibility on last segment start point
      foundValid = False
      for node in nextNodes:
        if isValidStartingNode(node, visited, graph, segment):
          start = node
          foundValid = True
          break
      if not foundValid:
        # print("warning:couldnt-find-valid-stating-node:{}".format(nextNodes))
        return graph, True 
    # need to know about next segment when creating the current segment in order to ensure
    # as a segment is constructed that we are always leaving sufficient space for the next segment
    # TODO: add this check in createSegment function
    rem = createSegment(visited, graph, start, segment, segments[i+1:], colors[i])
    for node in rem:
      nextNodes.append(node)
  return graph, False

def createSegment(visited, matrix, start, size, remainingSegments, color):
  """
  walk the matrix and create a segment of given size
  """
  nodesToPaint = [start]
  currentSize = 0
  unpaintedNodes = []
  while len(nodesToPaint) and currentSize < size:
    currentNode = nodesToPaint.pop()
    
    i = currentNode[0]
    j = currentNode[1]
    # check if this node is a valid node to paint
    if visited[i][j]:
      continue
    if remainingSegments:
      # edge cases:
      # 1. the node checked needs to factor in it might be last node of the segment
      # 2. the checking of remaining space for the next segment needs to be done not just
      #    for neighboring nodes of the given node but all unvisited remaining nodes unpainted
      # 3. play through creating remaining segments and validate its possible given paining the current
      #    node.
      while not isValidNode(i, j, matrix, visited, remainingSegments) and len(nodesToPaint):
        currentNode = nodesToPaint.pop()
        unpaintedNodes.append(currentNode)
        i = currentNode[0]
        j = currentNode[1]
    # print("found node at ({},{}) valid".format(i, j))
    # if not isValidNode(i, j, matrix, visited, nextSegment):
    #   print("warning invalid node: {}".format(currentNode))
    visited[i][j] = True
    
    matrix[i][j] = color
    currentSize += 1
    options = getNextSegmentNode(i, j, matrix, visited)
    
    for option in options:
      nodesToPaint.append(option)
  # print("nodesToPaint: {}".format(nodesToPaint))
  # print("unpaintedNodes: {}".format(unpaintedNodes))
  return nodesToPaint + unpaintedNodes


def isValidNode(i, j, matrix, visited, remainingSegments):
  """
  will check that IF this node is painted will there be space for the next segment (size)
  """
  nextSegment = sum(remainingSegments)
  tmpVisited = copy.deepcopy(visited)
  tmpMatrix = copy.deepcopy(matrix)
  tmpVisited[i][j] = True
  options = getNextSegmentNode(i, j, matrix, tmpVisited)
  if not options:
    return True
  # TODO: fix this as its a naive validating of the sum of remaining segments instead of
  # considering the discontiguous subsets i.e 4 vs 2 --> 2
  
  options = list(filter(lambda x: isValidStartingNode(x, tmpVisited, tmpMatrix, nextSegment), options))
  if len(options) > 0:
    return True
  else:
    return False

def isValidStartingNode(node, visited, matrix, segment):
  """
  responsible for checking if a given starting point will be viable for a segment
  needs to check:
  1. that the given starting node AND the subsequent next nodes will be valid
  2. 
  """
  nodesAvailable = [node]
  currentSize = 0
  tmpVisited = copy.deepcopy(visited)
  while len(nodesAvailable) and currentSize < segment:
    currentNode = nodesAvailable.pop()
    # print(currentNode)
    i = currentNode[0]
    j = currentNode[1]
    if tmpVisited[i][j]:
      continue
    tmpVisited[i][j] = True
    currentSize += 1
    nextNodes = getNextSegmentNode(i, j, matrix, tmpVisited)
    for node in nextNodes:
      i = node[0]
      j = node[1]
      nodesAvailable.append(node)
  if currentSize >= segment:
    return True
  else:
    return False


def getNextSegmentNode(i, j, matrix, visited):
  """
  randomly select next node to pain
  """
  options = []
  if j > 0 and not visited[i][j-1]:
    options.append([i, j-1])
  if j < len(matrix[0]) - 1 and not visited[i][j+1]:
    options.append([i, j+1])
  if i > 0 and not visited[i-1][j]:
    options.append([i-1, j])
  if i < len(matrix) - 1 and not visited[i+1][j]:
    options.append([i+1, j])
  # random.shuffle(options)
  return options

if __name__ == "__main__":

  # printGraph(3, 3,['r', 'g', 'b']) 
  printGraph(3, 3,['r', 'g', 'b'])