import numpy as np
import pathlib


def validate_mtx(matriz):
    # validates dimensions of MATRIZ nxm
    # if valid returns the number of lines and columns

    if isinstance(matriz, (int, float, complex, np.number)) or (
        isinstance(matriz, np.ndarray) and not matriz.shape
    ):
        raise ValueError(
            "A matrix should have lines and columns. Only a single value found."
        )
    lines = len(matriz)
    if not lines:
        raise ValueError("Invalid matrix! No values found.")
    if isinstance(matriz[0], (int, float, complex, np.number)):
        raise ValueError("A matrix should have lines and columns. Only lines found.")
    column = len(matriz[0])
    for i, line in enumerate(matriz[1:]):
        if len(line) != column:
            raise ValueError(
                f"Not valid matrix! Invalid number of elements for column {i + 2}"
            )
    return lines, i + 2  # i + 2 is the number of columns


def assert_same_mtx_size(a, b):
    assert a == b, (
        f"Sizes of matrices should be equal, but got {a} (left) and {b} (right)."
    )


class Matrib:
    def __init__(self, matriz):
        super().__init__()
        self.content = matriz
        # validation
        lines, columns = validate_mtx(matriz)

        self.lines = lines
        self.columns = columns
        self.size = (lines, columns)

    def __add__(self, nova_matriz):
        # method for sum +

        result = []
        # check compatibility
        assert_same_mtx_size(self.size, nova_matriz.size)

        for i in range(self.size[0]):
            result.append([])
            for j in range(self.size[1]):
                result[i].append(self.content[i][j] + nova_matriz.content[i][j])
        return self.__class__(result)

    def __mul__(self, nova_matriz):
        # method for multiplication *

        result = []
        # check compatibility
        assert_same_mtx_size(self.size, nova_matriz.size)

        for i in range(self.size[0]):
            result.append([])
            for j in range(self.size[1]):
                result[i].append(self.content[i][j] * nova_matriz.content[i][j])
        return self.__class__(result)

    def __matmul__(self, nova_matriz):
        # method for matrix multiplication @

        result = []
        # check compatibility
        assert self.columns == nova_matriz.lines, (
            "columns from the left matrix should be the same number of lines of the right matrix, but got "
            f" {self.columns} columns (left) and {nova_matriz.lines} lines (right)"
        )

        for i in range(self.lines):
            result.append([0] * self.columns)
            for j in range(self.columns):
                for ln in range(nova_matriz.lines):
                    result[i][j] += self.content[i][ln] * nova_matriz.content[ln][j]
        return self.__class__(result)

    def __str__(self):
        # find max for width
        width = 1  # min width
        values = []
        for i in range(self.lines):
            for j in range(self.columns):
                value = self.content[i][j]
                if isinstance(value, (float, np.float32, np.float64)):
                    value = round(value, 3)
                values.append(value)
                if width < (m := len(str(value))):
                    width = m
        space_bound = self.columns * (width + 1) - 1  # upper and lower bounds
        result = f"┌ {' ' * space_bound} ┐\n"
        seq = 0
        for i in range(self.lines):
            result += "│"
            for j in range(self.columns):
                result += f" {values[seq + j]:>{width}}"
            seq += j + 1
            result += " │\n"
        result += f"└ {' ' * space_bound} ┘"
        return result


def main():
    np.random.seed(0)
    a = Matrib(np.random.randint(0, 10, (10, 10)))
    b = Matrib(np.random.randint(0, 10, (10, 10)))
    file1 = pathlib.Path("artifacts/3_1_matrix_sum.txt")
    file2 = pathlib.Path("artifacts/3_1_matrix_mul.txt")
    file3 = pathlib.Path("artifacts/3_1_matrix_matmul.txt")

    with (
        open(file1, "w", encoding="utf-8") as f1,
        open(file2, "w", encoding="utf-8") as f2,
        open(file3, "w", encoding="utf-8") as f3,
    ):
        f1.write(str(a + b))
        f2.write(str(a * b))
        f3.write(str(a @ b))


if __name__ == "__main__":
    main()
