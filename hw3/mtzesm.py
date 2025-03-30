import numpy as np
import pathlib


def validate_mtx(matriz):
    # validates dimensions of MATRIZ nxm
    # if valid returns the number of lines and columns

    if isinstance(matriz, (int, float, complex, np.number)) or (isinstance(matriz, np.ndarray) and not matriz.shape):
        raise ValueError("A matrix should have lines and columns. Only a single value found.")
    lines = len(matriz)
    if not lines:
        raise ValueError("Invalid matrix! No values found.")
    if isinstance(matriz[0], (int, float, complex, np.number)):
        raise ValueError("A matrix should have lines and columns. Only lines found.")
    column = len(matriz[0])
    for i, line in enumerate(matriz[1:]):
        if len(line) != column:
            raise ValueError(f"Not valid matrix! Invalid number of elements for column {i+2}")
    return lines, i + 2   # i + 2 is the number of columns

def assert_same_mtx_size(a, b):
    assert a == b, \
            f"Sizes of matrices should be equal, but got {a} (left) and {b} (right)."


class Matrib(object):
    def __init__(self, matriz):
        super().__init__()
        self.content = matriz

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, val):
        raise NotImplementedError("Reshaping is not implemented")
  
    def __str__(self):

        # find max for width
        width = 1   # min width
        values = []
        for i in range(self._lines):
            for j in range(self._columns):
                value = self.content[i][j]
                if isinstance(value, (float, np.float32, np.float64)):
                    value = round(value, 3)
                values.append(value)
                if width < (m := len(str(value))):
                    width = m
        space_bound = self._columns * (width + 1) - 1    # upper and lower bounds
        result = f"┌ {' ' * space_bound} ┐\n"
        seq = 0
        for i in range(self._lines):
            result += "│"
            for j in range(self._columns):
                result += f" {values[seq+j]:>{width}}"
            seq += j + 1
            result += " │\n"
        result += f"└ {' ' * space_bound} ┘"
        return result
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value

        if name == "content":
            # validation
            lines, columns = validate_mtx(value)
            # setting more attributes
            self.__dict__["_lines"] = lines
            self.__dict__["_columns"] = columns
            self.__dict__["_size"] = (lines, columns)

    def __getattribute__(self, name):
        if name == "size":
            print("Warning: 'size' will be deprecated.")
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        raise AttributeError(f"There is no '{name}' attribute. "
                             "There are only two attributes: 'size' and 'content'")


class Matriz(Matrib, np.lib.mixins.NDArrayOperatorsMixin):
    pass


def main():
    np.random.seed(0)
    a = Matriz(np.random.randint(0, 10, (10, 10)))
    b = Matriz(np.random.randint(0, 10, (10, 10)))
    
    file1 = pathlib.Path("artifacts/3_2_matrix_sum.txt")
    file2 = pathlib.Path("artifacts/3_2_matrix_mul.txt")
    file3 = pathlib.Path("artifacts/3_2_matrix_matmul.txt")

    with open(file1, "w", encoding="utf-8") as f1, open(file2, "w", encoding="utf-8") as f2, open(file3, "w", encoding="utf-8") as f3:
        f1.write(str(a + b))
        f2.write(str(a * b))
        f3.write(str(a @ b))


if __name__ == "__main__":
    main()
