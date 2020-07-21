import random
import math
import copy

def getColor(color):
  d = {
    'r': '\033[1;31;40m',
    'b': '\033[1;34;40m',
    'g': '\033[1;32;40m',
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
  visited = [[False for col in range(width)] for row in range(height)]
  matrix = [['' for col in range(width)] for row in range(height)]
  start_j = random.randint(0, width-1) # col
  start_i = random.choice([0, height-1]) if start_j > 0 and start_j < width else random.randint(0, height-1) # row
  start = [start_i, start_j]
  combinations = random.choice(getCombinations(height * width))
  combinations.sort(reverse=True)
  print("combinations: {}".format(combinations))
  combinations=[4,4,1]
  nextNodes = []
  for i in range(len(combinations)):
    segment = combinations[i]
    nextSegment = combinations[i+1] if i < len(combinations) - 1 else 0
    if len(nextNodes):
    # two edges cases:
    # 1. check if next starting point has sufficient space for the next segment
    # 2. may be solved by 1. but need to have visibility on last segment start point
      foundValid = False
      for node in nextNodes:
        if isValidStartingNode(node, visited, matrix, segment):
          start = node
          foundValid = True
          break
      if not foundValid:
        print("warning:couldnt-find-valid-stating-node:{}".format(nextNodes))
    # need to know about next segment when creating the current segment in order to ensure
    # as a segment is constructed that we are always leaving sufficient space for the next segment
    # TODO: add this check in createSegment function
    rem = createSegment(visited, matrix, start, segment, nextSegment, colors[i])
    for node in rem:
      nextNodes.append(node)
   


  for i in range(height):
    for j in range(width):
      print("{}x{}".format(getColor(matrix[i][j]), getColor(matrix[i][j])), end="")
    print("")
def isValidStartingNode(node, visited, matrix, segmentSize):
  """
  responsible for checking if a given starting point will be viable for a segment
  """
  nodesAvailable = [node]
  print("nodesAvailable:{}:segment:{}".format(nodesAvailable, segmentSize))
  print(visited)
  currentSize = 0
  tmpVisited = copy.deepcopy(visited)
  while len(nodesAvailable) and currentSize < segmentSize:
    currentNode = nodesAvailable.pop()
    print(currentNode)
    i = currentNode[0]
    j = currentNode[1]
    if tmpVisited[i][j]:
      continue
    tmpVisited[i][j] = True
    currentSize += 1
    nextNodes = getNextSegmentNode(i, j, matrix, tmpVisited)
    for node in nextNodes:
      nodesAvailable.append(node)
  if currentSize >= segmentSize:
    return True
  else:
    return False
def createSegment(visited, matrix, start, size, nextSize, color):
  """
  walk the matrix and create a segment of given size
  """
  print("---segment:color:{}---".format(color))
  print("---segment:start:{}---".format(start))
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
    while not isValidNode(i, j, matrix, visited, nextSize) and len(nodesToPaint):
      print("warning invalid node: {}".format(currentNode))
      currentNode = nodesToPaint.pop()
      unpaintedNodes.append(currentNode)
      i = currentNode[0]
      j = currentNode[1]
    # if not isValidNode(i, j, matrix, visited, nextSize):
    #   print("warning invalid node: {}".format(currentNode))
    visited[i][j] = True
    
    matrix[i][j] = color
    currentSize += 1
    options = getNextSegmentNode(i, j, matrix, visited, nextSize)
    
    for option in options:
      nodesToPaint.append(option)
  print("nodesToPaint: {}".format(nodesToPaint))
  print("unpaintedNodes: {}".format(unpaintedNodes))
  return nodesToPaint + unpaintedNodes
def isValidNode(i, j, matrix, visited, nextSegmentsize):
  """
  will check that IF this node is painted will there be space for the next segment (size)
  """
  print("checking i: {}, j: {}, for next segment: {}".format(i, j, nextSegmentsize))
  tmpVisited = copy.deepcopy(visited)
  tmpVisited[i][j] = True
  options = getNextSegmentNode(i, j, matrix, tmpVisited)
  print(options)
  options = list(filter(lambda x: isValidStartingNode(x, tmpVisited, matrix, nextSegmentsize), options))
  if len(options) > 0:
    print(matrix)
    print(tmpVisited)
    print(options)
    return True
  else:
    return False
def getNextSegmentNode(i, j, matrix, visited, nextSize = None):
  """
  randomly select next node to pain
  """
  options = []
  if i > 0 and not visited[i-1][j]:
    options.append([i-1, j])
  if i < len(matrix) - 1 and not visited[i+1][j]:
    options.append([i+1, j])
  if j > 0 and not visited[i][j-1]:
    options.append([i, j-1])
  if j < len(matrix[0]) - 1 and not visited[i][j+1]:
    options.append([i, j+1])
  # filter invalid options based on next size
  # if nextSize:
  #   options = list(filter(lambda x: isValidStartingNode(x, visited, matrix, nextSize), options))
  # if not len(options) and nextSize:
  #   print("warning filtered all results for nextSize: {}".format(nextSize))
  random.shuffle(options)
  return options




if __name__ == "__main__":

  printGraph(3, 3,['r', 'g', 'b']) 