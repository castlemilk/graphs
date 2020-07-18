import random
import math

def getColor(color):
  d = {
    'r': '\033[1;31;40m',
    'b': '\033[1;34;40m',
    'g': '\033[1;32;40m',
    '': '\033[1;30;40m'
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
  print("combinations: {}".format(combinations))
  for index, segment in enumerate(combinations):
    print("start: {}".format(start))
    start = createSegment(visited, matrix, start, segment, colors[index])
  for i in range(height):
    for j in range(width):
      print("{}x{}".format(getColor(matrix[i][j]), getColor(matrix[i][j])), end="")
    print("")
def createSegment(visited, matrix, start, size, color):
  """
  walk the matrix and create a segment of given size
  """
  print("---segment:color:{}---".format(color))
  print("---segment:start:{}---".format(start))
  nodesToPaint = [start]
  currentSize = 0
  while len(nodesToPaint) and currentSize < size:
    currentNode = nodesToPaint.pop()
    i = currentNode[0]
    j = currentNode[1]
    if visited[i][j]:
      continue
    visited[i][j] = True
    
    matrix[i][j] = color
    currentSize += 1
    options = getNextSegmentNode(i, j, matrix, visited)
    for option in options:
      nodesToPaint.append(option)
    print(nodesToPaint)
  return nodesToPaint.pop() if len(nodesToPaint) else []

def getNextSegmentNode(i, j, matrix, visited):
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
  print("options:{}".format(options))
  # if len(options):
  #   nextNode = random.choice(options)
  #   return nextNode
  # else:
  #   return []
  return options 




if __name__ == "__main__":

  printGraph(3, 3,['r', 'g', 'b']) 