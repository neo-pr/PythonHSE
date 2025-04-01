import numpy as np
import pathlib
import pickle

CACHE_DIR = pathlib.Path("mtxesm_mul_cache")


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


def save_cache_mul(hash_a, hash_b, result):
    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir()

    # openinig/creating file
    with open(CACHE_DIR.joinpath(f"{hash_a}.pickle"), "ab") as f:
        pickle.dump((hash_b, result), f)


def read_cache_mul(hash_a, hash_b):
    if not CACHE_DIR.exists():
        return None

    cache_file = CACHE_DIR.joinpath(f"{hash_a}.pickle")
    if pathlib.Path.exists(cache_file):
        with open(cache_file, "rb") as f:
            try:
                while (hb := pickle.load(f))[0] != hash_b:
                    ...
                return hb[1]
            except EOFError:
                pass

    return None


class Matrihs:
    def __eq__(self, other):
        # first check shape
        if self.size == other.size:
            # checking components
            for i in range(self.lines):
                for j in range(self.columns):
                    if self.content[i][j] != other.content[i][j]:
                        return False
            else:
                return True
        # size is different
        return False

    def __hash__(self):
        """
        The hash is buil based on:
        1- the flattened array (tuple)
        and (+)
        2- its size (tuple)
        """

        return hash(tuple(n for line in self.content for n in line) + self.size)


class Matrib:
    def __init__(self, matriz):
        super().__init__()
        self.content = matriz
        # validation
        lines, columns = validate_mtx(matriz)

        self.lines = lines
        self.columns = columns
        self.size = (lines, columns)

        self.use_cache = True

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

        # check for cached mat multiplications
        # if use_cache and (res := read_cache_mul(hash(self), hash(nova_matriz))):
        if self.use_cache:
            hash_a, hash_b = hash(self), hash(nova_matriz)
            if res := read_cache_mul(hash_a, hash_b):
                print("returned from cached")  # temp DELETE this line
                return res

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

        res = self.__class__(result)
        # caching
        if self.use_cache:
            save_cache_mul(hash_a, hash_b, res)

        return res

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


class Matriz(Matrib, Matrihs):
    pass


def main():
    np.random.seed(0)
    a = Matriz([[0, 1], [-1, 2]])
    b = Matriz([[1, 2], [2, 1]])
    c = Matriz([[0, 1], [-2, 2]])
    d = Matriz([[1, 2], [2, 1]])

    # mat multiplications
    ab = a @ b
    # cd will be from cached as hash a == hash c and b == d
    cd_cached = c @ d
    # getting real cd
    c.use_cache = False
    cd = c @ d

    # asserting conditions
    assert (hash(a) == hash(c)) and (a != c) and (b == d) and (ab != cd)

    # saving matrices files
    for obj, fname in zip([a, b, c, d, ab, cd], ["A", "B", "C", "D", "AB", "CD"]):
        file = pathlib.Path(f"artifacts/{fname}.txt")
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(obj))

    # saving hash file
    with open(pathlib.Path("artifacts/hash.txt"), "w", encoding="utf-8") as f:
        f.write(f"hash matrix AB:   {hash(ab)}\n")
        f.write(f"hash matrix CD:   {hash(cd)}\n")
        f.write(f"hash CD (cached): {hash(cd_cached)}\n")


if __name__ == "__main__":
    main()
