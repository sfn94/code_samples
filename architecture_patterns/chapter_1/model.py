

from datetime import date
from dataclasses import dataclass
# https://docs.python.org/3/library/typing.html
# https://realpython.com/python-type-checking/
from typing import Optional, NewType


Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)


# https://realpython.com/python-data-classes/  read more
@dataclass(frozen = True)   
class OrderLine:
    orderid : str
    sku : str
    qty : int


class Batch():
    def __init__(self, ref : Reference, Sku : Sku, qty : Quantity , eta : Optional[date]):
        self.ref = ref
        self.sku = Sku 
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set() # type: Set[OrderLine]
        # self.available_quantity = quantity
        # self.allocated_lines = set()

    # @property decorator https://www.youtube.com/watch?v=jCzT9XFZ5bw
    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
        # we can't allocate the same line twie 

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


if __name__=="__main__":
    line = OrderLine("IDA32342", "CHAISE", 5)

    print("start")
    print("end")


