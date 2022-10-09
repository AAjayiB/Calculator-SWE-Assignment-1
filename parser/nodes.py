from copy import deepcopy
from itertools import groupby
from operator import add, mul, pow, sub

from .utils import after_traverse


class Node(object):
    NAME = 'node'

    def __repr__(self):
        return f"<{self.__class__.NAME} {', '.join([k + '=' + str(v) for k, v in self.__dict__.items()])}>"

    def clone(self):
        return self.__class__()


class SingleValueNode(Node):
  
    def __init__(self, value):
        self.value = value

    def clone(self):
        if hasattr(self.value, "clone"):
            copy_value = self.value.clone()
        else:
            copy_value = deepcopy(self.value)

        return self.__class__(copy_value)


class Number(SingleValueNode):
    NAME = 'number'

    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError()
        super().__init__(value)


class Variable(SingleValueNode):

    NAME = 'variable'

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError()
        super().__init__(value)



class BinExpr(Node):
    NAME = 'binExpr'
    OP = ''

    _OPS = {
        '+': add,
        '-': sub,
        '*': mul,
        '^': pow,
    }

    def __init__(self, l_value, r_value):
        self.l_value = l_value
        self.r_value = r_value

    @property
    def value(self):
        return self.OP

    @property
    def op_method(self):
        return BinExpr._OPS[self.OP]

    def clone(self):
        if hasattr(self.l_value, "clone"):
            copy_l_value = self.l_value.clone()
        else:
            copy_l_value = deepcopy(self.l_value)

        if hasattr(self.r_value, "clone"):
            copy_r_value = self.r_value.clone()
        else:
            copy_r_value = deepcopy(self.r_value)

        return self.__class__(copy_l_value, copy_r_value)

    def __repr__(self):
        return f"<{self.__class__.NAME} '{self.__class__.OP}' " \
            f" {', '.join([k + '=' + str(v) for k, v in self.__dict__.items()])} > "


class Add(BinExpr):
    """add"""
    OP = '+'


class Sub(BinExpr):
    """subtract"""
    OP = '-'


class Mul(BinExpr):
    """multiply"""
    OP = '*'


class Pow(BinExpr):
    """power"""
    OP = '^'


item_wrapper_dict = {
    "item": lambda value: value,
    "number": lambda value: Item(value.value),
    "variable": lambda value: Item(1, SubItem(**{value.value: 1}))
}


def node2item_wrapper(node):
    return item_wrapper_dict[node.__class__.__name__.lower()](node)


class MPExpression(object):
    """Multivariate expression"""
    def __init__(self, root_node):
        self._vars = set()
        self.root_node = root_node

        calc_stack = []

        def calc(node):
            if isinstance(node, BinExpr):
                rhs = calc_stack.pop()
                lhs = calc_stack.pop()
                result = node.op_method(lhs, rhs)
                calc_stack.append(result)
            else:
                wrapped_item = node2item_wrapper(node)
                calc_stack.append(wrapped_item)


        after_traverse(root_node, calc)
        result = calc_stack[0]
        if isinstance(result, Item):
            self._value = MultielementPolynomial(result)
        self._value = result

    def __eq__(self, other):
        if not isinstance(other, MPExpression):
            raise TypeError()
        return self.value == other.value

    @property
    def vars(self):
        return self._vars

    @property
    def value(self):
        return self._value


class MultielementPolynomial(Node):
    def __init__(self, *items):
        self.items = [item for item in items
                      if item.coefficient != 0]  
        self.merge_similar_items()
        self.items.sort(reverse=False)

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        buffer = []
        for i, item in enumerate(self.items):
            if i == 0 and item.coefficient != 0:  
                buffer.append(item)
            else:
                if item.coefficient > 0:
                    buffer.append("+")
                    buffer.append(item)
                elif item.coefficient < 0:
                    buffer.append(item)

        if not buffer:
            buffer.append(Item(0))

        return ''.join([str(i) for i in buffer])

    def merge_similar_items(self):
        items = self.items.copy()

        work_list = []
        result_list = []


        while items:
            refer = items.pop()
            work_list.append(refer)
            work_list.extend(
                (item for item in items if item.sub_item == refer.sub_item))
            for item in work_list[1:]:
                items.remove(item)
                work_list[0] += item
            assert isinstance(
                work_list[0],
                Item)  
            result_list.append(work_list[0])
            work_list.clear()
        self.items = result_list

    def add_or_sub(self, other, flag: bool):
        other_items = other.items if isinstance(
            other, MultielementPolynomial) else [node2item_wrapper(other)]
        if not flag:  
            other_items = [-item for item in other_items]
        return MultielementPolynomial(*(self.items + other_items))

    def __add__(self, other):
        return self.add_or_sub(other, True)

    def __sub__(self, other):
        return self.add_or_sub(other, False)

    def __mul__(self, other):
        retVal = Item()
        if isinstance(other, MultielementPolynomial):
            for item_1 in self.items:
                for item_2 in other.items:
                    retVal += item_1 * item_2
        elif isinstance(other, (Item, Number, Variable, int, float)):
            for item in self.items:
                retVal += item * other
        else:
            raise TypeError()

        return retVal

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            result = self
            for _ in range(power.value):
                result *= self
            return result
        else:
            raise NotImplementedError("Other types of power are not supported temporarily!!!")

    def __eq__(self, other):
        if not isinstance(other, MultielementPolynomial):
            raise TypeError()
        return self.items == other.items


class Item(Node):
    def __init__(self, coefficient=0, sub_item=None):
        self.coefficient = coefficient
        self.sub_item = sub_item or SubItem()

    def __str__(self):
        if not self.sub_item.is_empty and self.coefficient == 1:
            if self.coefficient == 1:
                return f"{self.sub_item}"
            if self.coefficient == 0:
                return f"{self.coefficient}"

        return f"{self.coefficient}{self.sub_item}"

    def __neg__(self):
        return Item(-self.coefficient, self.sub_item)

    def __add__(self, other):
        if isinstance(other, Item):
            if (self.sub_item == other.sub_item):
                coefficient_result = self.coefficient + other.coefficient
                return Item(coefficient_result, self.sub_item)
            return MultielementPolynomial(self, other)
        elif isinstance(other, (MultielementPolynomial, Number, Variable)):
            return MultielementPolynomial(self) + other
        else:
            raise TypeError()

    def __sub__(self, other):
        if isinstance(other, Item):
            if (self.sub_item == other.sub_item):
                coefficient_result = self.coefficient - other.coefficient
                return Item(coefficient_result, self.sub_item)
            return MultielementPolynomial(self, -other)
        elif isinstance(other, (MultielementPolynomial, Number, Variable)):
            return MultielementPolynomial(self) - other
        else:
            raise TypeError()

    def __mul__(self, other):
        if isinstance(other, Item):
            return Item(self.coefficient * other.coefficient,
                        self.sub_item * other.sub_item)
        elif isinstance(other, MultielementPolynomial):
            return MultielementPolynomial(self) * other
        elif isinstance(other, Number):
            return Item(self.coefficient * other.value, self.sub_item)
        elif isinstance(other, Variable):
            return Item(self.coefficient, self.sub_item * other)
        else:
            raise TypeError()

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            return Item(self.coefficient**power.value, self.sub_item**power)
        elif isinstance(power, Item) and power.sub_item.is_empty:
            return Item(self.coefficient**power.coefficient,
                        self.sub_item**power.coefficient)
        else:
            raise NotImplementedError("Other types of power are not supported temporarily!!!")

    def __lt__(self, other):
        if isinstance(other, Item):
            if self.sub_item.is_empty and other.sub_item.is_empty:
                return self.coefficient < other.coefficient
            return self.sub_item < other.sub_item
        else:
            raise TypeError()

    def __eq__(self, other):
        if not isinstance(other, Item):
            raise TypeError()
        if self.coefficient != other.coefficient:
            return False
        return self.sub_item == other.sub_item


class SubItem(Node):
    def __init__(self, **kwargs):
        self.var_pow_dict = kwargs

    @property
    def is_empty(self):
        return not bool(self.var_pow_dict)

    def __str__(self):
        buffer = []
        for c, e in sorted(self.var_pow_dict.items()):
            if e == 1:
                buffer.append(f"{c}")
            else:
                buffer.append(f"{c}^{e}")
        return "*".join(buffer)

    def __eq__(self, other):
        if isinstance(other, SubItem):
            return self.var_pow_dict == other.var_pow_dict

    def __getitem__(self, item):
        return self.var_pow_dict.get(item, 0)

    def __mul__(self, other):
        if isinstance(other, SubItem):
            new_var_pow_dict = self.var_pow_dict.copy()

            for k, v in other.var_pow_dict.items():
                if k in new_var_pow_dict:
                    new_var_pow_dict[k] += v
                else:
                    new_var_pow_dict[k] = v

        elif isinstance(other, Variable):
            new_var_pow_dict = self.var_pow_dict.copy()

            if other.value in new_var_pow_dict:
                new_var_pow_dict[other.value] += 1
            else:
                new_var_pow_dict[other.value] = 1
        else:
            raise TypeError()

        return SubItem(**new_var_pow_dict)

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            return SubItem(
                **{k: v * power.value
                   for k, v in self.var_pow_dict.items()})
        elif isinstance(power, (int, float)):
            return SubItem(
                **{k: v * power
                   for k, v in self.var_pow_dict.items()})
        else:
            raise NotImplementedError("暂不支持幂为其他类型的情况")

    def __lt__(self, other):
        if isinstance(other, SubItem):
            if self.is_empty or other.is_empty:
                if self.is_empty and not other.is_empty:
                    return False
                elif not self.is_empty and other.is_empty:
                    return True
                return False
            if self.var_pow_dict.keys() != other.var_pow_dict.keys():
                all_var_set = self.var_pow_dict.keys(
                ) | other.var_pow_dict.keys()
                min_var = min(all_var_set)
                return min_var in self.var_pow_dict.keys()
            for var in sorted(self.var_pow_dict.keys()):
                if self.var_pow_dict[var] == other.var_pow_dict[var]:
                    continue
                return self.var_pow_dict[var] < other.var_pow_dict[var]
        else:
            raise TypeError()
