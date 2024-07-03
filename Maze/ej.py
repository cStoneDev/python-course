from collections import deque

def initialize_visited(rows, cols):
    return [[False for _ in range(cols)] for _ in range(rows)]

def find_path_bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = initialize_visited(rows, cols)
    queue = deque([(start, [start])])
    visited[start[0]][start[1]] = True
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        (i, j), path = queue.popleft()
        
        if (i, j) == goal:
            return path
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            
            if 0 <= ni < rows and 0 <= nj < cols and not visited[ni][nj] and maze[ni][nj] == 0:
                visited[ni][nj] = True
                queue.append(((ni, nj), path + [(ni, nj)]))
    
    return []


maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)  # Nodo inicial
goal = (4, 4)   # Nodo objetivo

path = find_path_bfs(maze, start, goal)
print(path)