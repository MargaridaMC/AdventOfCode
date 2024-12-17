import numpy as np
def parse_input_to_np_2d_array(data: str) -> np.array:
    return np.array([[e for e in row] for row in data.splitlines()])