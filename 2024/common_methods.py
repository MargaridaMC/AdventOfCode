import numpy as np

def get_shortest_path_from_matrix(allowed_map_locations, start_pos, end_pos) -> list | None:
    
    """
    Uses the Djisktra algorithm to find the length of the shortest path between two points on a 2D grid.
    Args:
        allowed_map_locations (np.array): A 2D grid where 0 represents an allowed location and 1 represents a wall.
        start_pos (tuple): A tuple representing the starting position (x, y) on the grid.
        end_pos (tuple): A tuple representing the ending position (x, y) on the grid.
    Returns:
        list: A list of tuples representing the shortest path between the start and end positions. Returns None if no path is found
    """

    def reorder_path(previous_nodes):
        shortest_path = [end_pos]
        current_node = end_pos
        while current_node != start_pos:
            current_node = previous_nodes[current_node]
            shortest_path = [current_node] + shortest_path
        return shortest_path
    
    previous_nodes = dict()

    rows, cols = allowed_map_locations.shape
    checked_positions = np.zeros_like(allowed_map_locations, dtype=int)
    checked_positions[*start_pos] = 1
    distances = [(start_pos, 0)]

    while True:
        closest_position, closest_distance = distances.pop(0)
        checked_positions[*closest_position] = 1
        for (x_dir, y_dir) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_position = (closest_position[0] + x_dir, closest_position[1] + y_dir)
            
            if 0 <= next_position[0] < rows and 0 <= next_position[1] < cols and allowed_map_locations[*next_position] != 1 and checked_positions[*next_position] == 0:
                if next_position == end_pos:
                    previous_nodes[next_position] = closest_position
                    return reorder_path(previous_nodes)

                distances.append((next_position, closest_distance + 1))
                previous_nodes[next_position] = closest_position
                checked_positions[*next_position] = 1
        
        if len(distances) == 0:
            return None

        # Sort distance list by distance
        distances = sorted(distances, key=lambda x: x[1])