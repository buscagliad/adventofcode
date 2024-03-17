from collections import deque

def shortest_distance(grid, start, end):
    rows = len(grid)
    cols = len(grid[0])
    
    # Define directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Queue for BFS
    queue = deque([(start, 0)])
    
    # Set to track visited cells
    visited = set([start])
    
    # BFS
    while queue:
        (x, y), distance = queue.popleft()
        
        if (x, y) == end:
            return distance
        
        # Explore neighbors
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if 0 <= new_x < rows and 0 <= new_y < cols and grid[new_x][new_y] == '.' and (new_x, new_y) not in visited:
                queue.append(((new_x, new_y), distance + 1))
                visited.add((new_x, new_y))
    
    # If no path found
    return -1

# Example usage:
grid = [
    ['.', '#', '.', '.', '.'],
    ['.', '.', '.', '#', '.'],
    ['#', '.', '#', '.', '.'],
    ['.', '#', '.', '.', '.']
]
start = (0, 0)
end = (2, 4)

print("Shortest distance:", shortest_distance(grid, start, end))
