import time
import random

class GF2_191:
    IRREDUCIBLE_POLY = int("1" + "0" * 181 + "1" + "0" * 8 + "1", 2) # x^191 + x^9 + 1

    def __init__(self, value):
        self.value = value & ((1 << 191) - 1)

    def __str__(self):
        return hex(self.value)[2:].upper().zfill((191 + 3) // 4)

    @staticmethod
    def zero():
        return GF2_191(0)

    @staticmethod
    def one():
        return GF2_191(1)

    def add(self, other):
        return GF2_191(self.value ^ other.value)

    def multiply(self, other):
        result = 0
        a = self.value
        b = other.value

        for i in range(191):
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & (1 << 191):
                a ^= GF2_191.IRREDUCIBLE_POLY

        return GF2_191(result)

    def square(self):
        result = 0
        current = self.value

        for i in range(191):
            if (current & (1 << i)):
                result ^= (1 << (2 * i))

        for i in range(382, 190, -1):
            if result & (1 << i):
                result ^= GF2_191.IRREDUCIBLE_POLY << (i - 191)

        return GF2_191(result)

    def inverse(self):
        if self.value == 0:
            raise ValueError("Обернений елемент до 0 не існує.")

        a, b = self.value, GF2_191.IRREDUCIBLE_POLY
        u, v = 1, 0
        while a != 1:
            if a == 0:
                raise ValueError("Обернений елемент не знайдено.")

            shift = a.bit_length() - b.bit_length()
            if shift < 0:
                a, b = b, a
                u, v = v, u
                continue

            a ^= b << shift
            u ^= v << shift

            a &= (1 << 191) - 1
            u &= (1 << 191) - 1

        return GF2_191(u)

    def power(self, n):
        result = GF2_191.one()
        base = self

        while n > 0:
            if n & 1:
                result = result.multiply(base)
            base = base.square()
            n >>= 1

        return result

    @staticmethod
    def from_input():
        while True:
            try:
                hex_value = input("Введіть значення елемента в 16-вому форматі (до 191 біт): ").strip()
                value = int(hex_value, 16)
                if value >= (1 << 191):
                    raise ValueError("Число перевищує 191 біт.")
                return GF2_191(value)
            except ValueError as e:
                print(f"Помилка: {e}. Спробуйте ще раз.")

    @staticmethod
    def random_element():
        return GF2_191(random.randint(0, (1 << 191) - 1))


def validate_field_properties():
    print("\n Перевірка тотожностей ")
    a = GF2_191.random_element()
    b = GF2_191.random_element()
    c = GF2_191.random_element()
    d = GF2_191.random_element()

    left = a.add(b).multiply(c)
    right = a.multiply(c).add(b.multiply(c))
    assert left.value == right.value, "(a + b) * c != a * c + b * c"
    print("Тотожність (a + b) * c = a * c + b * c виконується")

    if d.value != 0:
        inv_d = d.inverse()
        one = d.multiply(inv_d)
        assert one.value == GF2_191.one().value, "d * d^(-1) != 1"
        print("Тотожність d * d^(-1) = 1 виконується")

    print("Усі перевірки успішні")


def measure_execution_time():
    print("\n Вимірювання часу ")
    operations = {
        "Додавання": lambda a, b: a.add(b),
        "Множення": lambda a, b: a.multiply(b),
        "Квадрат": lambda a, _: a.square(),
        "Обернений елемент": lambda a, _: a.inverse() if a.value != 0 else None,
        "Піднесення до степеня": lambda a, _: a.power(random.randint(0, (1 << 191) - 1))
    }

    timings = {}
    iterations = 1000
    for name, operation in operations.items():
        total_time = 0
        for _ in range(iterations):
            a = GF2_191.random_element()
            b = GF2_191.random_element()
            start = time.time()
            operation(a, b)
            end = time.time()
            total_time += (end - start)
        avg_time = total_time / iterations
        timings[name] = avg_time

    print("Результати вимірювань (у секундах):")
    for op, timing in timings.items():
        print(f"{op}: {timing:.6f} сек.")

    return timings


def main():
    a = GF2_191.from_input()
    b = GF2_191.from_input()
    n = int(input("Введіть степінь у 16-вій системі: ").strip(), 16)

    print(f"A: {a}")
    print(f"B: {b}")
    print(f"N: {hex(n).upper()[2:]}")

    zero = GF2_191.zero()
    one = GF2_191.one()
    print(f" (0): {zero}")
    print(f" (1): {one}")

    sum_ab = a.add(b)
    print(f"A+B: {sum_ab}")

    product_ab = a.multiply(b)
    print(f"A*B: {product_ab}")

    squared_a = a.square()
    print(f"А^2: {squared_a}")

    inv_a = a.inverse()
    print(f"A^(-1): {inv_a}")

    power_a = a.power(n)
    print(f"A^N: {power_a}")

    validate_field_properties()

    measure_execution_time()


if __name__ == "__main__":
    main()