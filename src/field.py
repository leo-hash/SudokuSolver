from dataclasses import dataclass, field
from pympler import asizeof
from bitarray import bitarray

def check_value(value):
    if not (0 < value < 10):
        raise ValueError(f"value {value} must be between 1 and 9")


@dataclass(slots=True)
class Field:
    _number: int | None = None
    _pos_number: bitarray = field(
        default_factory=lambda: bitarray('111111111')
    )

    def __post_init__(self):
        if self._number is not None:
            check_value(self._number)
            self.pos_number = {self._number}

    def is_posibile(self, value: int) -> bool:
        check_value(value)
        if self._pos_number[value-1] == 1:
            return True
        return False

    def set_posibile(self, value: int):
        # Necessary? ideally, pos_numbers should only get smaller
        # and backtracking to old state gets grid from stack
        raise NotImplementedError()

    def delete_posibile(self, value: int):
        check_value(value)
        self._pos_number[value-1] = 0

    def possible_count(self) -> int:
        count = 0
        for num in self._pos_number:
            if num == 1:
                count += 1
        return count

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value: int):
        check_value(value)
        if self._pos_number[value-1] == 0:
            raise ValueError(f"Number {value} not in List of possible numbers")

        self._number = value
        # set all pos_numbers except self.number to 0
        self.pos_number = {value}

    @property
    def pos_number(self) -> set[int]:
        numbers = set()
        for i in range(9):
            if self._pos_number[i] == 1:
                numbers.add(i + 1)
        return numbers

    @pos_number.setter
    def pos_number(self, value: set[int]):
        self._pos_number = bitarray('000000000')
        for cur in value:
            check_value(cur)
            self._pos_number[cur-1] = 1

    def __str__(self):
        return f"{self.number}"

if __name__ == '__main__':
    field = Field(_number=1)
    print(f"An instance of Field has a size of {asizeof.asizeof(field)} bytes.")
