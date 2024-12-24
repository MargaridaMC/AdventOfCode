import numpy as np
def parse_input_to_np_2d_array(data: str, convert_to_int = False) -> np.array:
    result = np.array([[e for e in row] for row in data.splitlines()])
    if convert_to_int:
        result = result.astype(int)
    return result