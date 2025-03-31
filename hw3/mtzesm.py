import numbers
import pathlib
import numpy as np


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


class Matrib(object):
    def __init__(self):
        self._content = None

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        raise NotImplementedError("Reshaping is not implemented")

    def __str__(self):
        # find max for width
        width = 1  # min width
        values = []
        for i in range(self._lines):
            for j in range(self._columns):
                number = self._content[i][j]
                if isinstance(number, (float, np.float32, np.float64)):
                    number = round(number, 3)
                values.append(number)
                if width < (m := len(str(number))):
                    width = m
        space_bound = self._columns * (width + 1) - 1  # upper and lower bounds
        result = f"┌ {' ' * space_bound} ┐\n"
        seq = 0
        for i in range(self._lines):
            result += "│"
            for j in range(self._columns):
                result += f" {values[seq + j]:>{width}}"
            seq += j + 1
            result += " │\n"
        result += f"└ {' ' * space_bound} ┘"
        return result

    def save(self, file_path):
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.__str__())

    @property
    def value(self):
        return self._content

    @value.setter
    def value(self, value):
        # validation
        lines, columns = validate_mtx(value)

        # setting the attribute
        self._content = value

        # setting extra attributes
        self._lines = lines
        self._columns = columns
        self._size = (lines, columns)

    def __getattribute__(self, name):
        if name == "size":
            print("Warning: 'size' will be deprecated.")
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        raise AttributeError(
            f"There is no '{name}' attribute. "
            "There are only two attributes: 'size' and 'content'"
        )


class ArrayLike(np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, value):
        super().__init__()

        self.value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (ArrayLike, Matriz)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, ArrayLike) else x for x in inputs)
        if out:
            kwargs["out"] = tuple(
                x.value if isinstance(x, ArrayLike) else x for x in out
            )
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == "at":
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.value)


class Matriz(ArrayLike, Matrib):
    pass


def main():
    np.random.seed(0)
    a = Matriz(np.random.randint(0, 10, (10, 10)))
    b = Matriz(np.random.randint(0, 10, (10, 10)))

    file1 = "artifacts/3_2_matrix_sum.txt"
    file2 = "artifacts/3_2_matrix_mul.txt"
    file3 = "artifacts/3_2_matrix_matmul.txt"

    (a + b).save(file1)
    (a * b).save(file2)
    (a @ b).save(file3)


if __name__ == "__main__":
    main()
