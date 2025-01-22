import decimal
import math
import re
from enum import Enum, auto
from typing import List, Union


class ReType(Enum):
    FAMOUS = auto()  # 有名分组
    UNKNOWN = auto()  # 无名分组
    MORE_ARGS = auto()  # 不确定参数个数无名分组


class FormulaConversion:

    def __init__(self, re_str: str, func, number_names: Union[None, List, str] = None):
        re_str_format_count = re_str.count("{}")
        args = []
        if number_names is None:
            self._re_type = ReType.UNKNOWN
            for index in range(re_str_format_count):
                args.append(self.get_number_matching_unknown_re_string())
        elif number_names == "more" and re_str_format_count == 1:
            self._re_type = ReType.MORE_ARGS
            args.append(self.get_more_number_matching_re_string())
        elif isinstance(number_names, list):
            self._re_type = ReType.FAMOUS
            if re_str_format_count != len(number_names):
                raise Exception("参数个数对不上")
            for args_key in number_names:
                args.append(self.get_number_matching_famous_re_string(args_key))
        else:
            raise Exception("没有这个类型")
        re_str = re_str.format(*args)
        self._re_obj = re.compile(re_str)
        self._re_func = func

    def check_formula(self, formula_str):
        compute_result = None
        while True:
            formula_str_re_result = self._re_obj.search(formula_str)
            if formula_str_re_result is None:
                if self.is_number(formula_str):
                    compute_result = self._check_number(formula_str)
                return formula_str, compute_result
            else:
                if self._re_type == ReType.FAMOUS:
                    func_kwargs = {}
                    for key, number_str in formula_str_re_result.groupdict().items():
                        number = self._check_number(number_str)
                        func_kwargs[key] = number
                    compute_result = self._re_func(**func_kwargs)
                elif self._re_type == ReType.MORE_ARGS:
                    func_args = []
                    formula_str_re_result_dict = formula_str_re_result.groupdict()
                    start_args_str = formula_str_re_result_dict.get("start_args")
                    other_args_str = formula_str_re_result_dict.get("other_args")
                    func_args.append(self._check_number(start_args_str))
                    other_args_str_list = other_args_str.split(",")
                    if len(other_args_str_list) != 0:
                        if other_args_str_list[0].strip() == "":
                            other_args_str_list.pop(0)
                        if len(other_args_str_list) != 0:
                            if other_args_str_list[-1].strip() == "":
                                other_args_str_list.pop(-1)
                            for number_str in other_args_str_list:
                                number_str = number_str.strip()
                                func_args.append(self._check_number(number_str))
                    compute_result = self._re_func(*func_args)
                else:
                    func_args = []
                    formula_str_re_result_list = formula_str_re_result.groups()
                    for formula_str_re_result_list_index in range(0, len(formula_str_re_result_list), 2):
                        number_str = formula_str_re_result_list[formula_str_re_result_list_index]
                        if formula_str_re_result_list[formula_str_re_result_list_index + 1] is not None:
                            number_str = '{}{}'.format(number_str, formula_str_re_result_list[formula_str_re_result_list_index + 1])
                        number = self._check_number(number_str)
                        func_args.append(number)
                    compute_result = self._re_func(*func_args)
                formula_str = "{}{}{}".format(formula_str[:formula_str_re_result.start()], compute_result, formula_str[formula_str_re_result.end():])

    @classmethod
    def _check_number(cls, number_str):
        is_negative_number = False
        if number_str.startswith("-"):
            is_negative_number = True
            number_str = number_str[1:]
        if number_str.isdigit():
            number = int(number_str)
        else:
            number = float(number_str)
        if is_negative_number:
            number = number
        return number

    @classmethod
    def get_number_matching_famous_re_string(cls, key_name):
        number_matching_re_string = " *(?P<{}>-?\d+\.*\d*(e-\d*)?) *".format(key_name)
        return number_matching_re_string

    @classmethod
    def get_number_matching_unknown_re_string(cls):
        number_matching_re_string = " *(-?\d+\.*\d*(e-\d*)?) *"
        return number_matching_re_string

    @classmethod
    def get_more_number_matching_re_string(cls):
        more_number_matching_unknown_re_string = ",?{}(?P<other_args>(,{})*),{{0,1}}".format(cls.get_number_matching_famous_re_string("start_args"),
                                                                                             cls.get_number_matching_unknown_re_string())
        return more_number_matching_unknown_re_string

    @classmethod
    def is_number(cls, number_str):
        is_number_re_result = re.search("^{}$".format(cls.get_number_matching_unknown_re_string()), number_str)
        if is_number_re_result is not None:
            return True
        return False


class FormulaConversionManager:
    bracket_formula_start_re = re.compile("\(")
    bracket_formula_start_and_end_re = re.compile("\(|\)")

    def __init__(self):
        self._formula_conversion_vector: List[FormulaConversion] = []

    def add_formula_conversion(self, re_str, func, number_names=None):
        formula_conversion = FormulaConversion(re_str, func, number_names=number_names)
        self._formula_conversion_vector.append(formula_conversion)

    def _check_formula(self, formula_str, get_number_type=False):
        for formula_conversion in self._formula_conversion_vector:
            formula_str, formula_str_result = formula_conversion.check_formula(formula_str)
            if formula_str.strip() == str(formula_str_result):
                if get_number_type:
                    return formula_str_result
                return formula_str
        return formula_str

    def _handle_formula(self, formula_str, start_index=None, get_number_type=True):
        while True:
            if start_index is not None:
                bracket_formula_re_result = self.bracket_formula_start_and_end_re.search(formula_str[start_index:])
            else:
                bracket_formula_re_result = self.bracket_formula_start_re.search(formula_str)

            if bracket_formula_re_result is not None:
                if bracket_formula_re_result.group() == "(":
                    new_start_index = bracket_formula_re_result.end()
                    if start_index is not None:
                        new_start_index = start_index + new_start_index
                    formula_str = self._handle_formula(formula_str, start_index=new_start_index)
                else:
                    end_index = bracket_formula_re_result.start()
                    if start_index is not None:
                        end_index = start_index + end_index
                    formula_str = "{}{}{}".format(formula_str[:start_index - 1], self._check_formula(formula_str[start_index:end_index]), formula_str[end_index + 1:])
                    return formula_str

            elif start_index is not None:
                raise Exception("公式格式错误")
            else:

                return self._check_formula(formula_str, get_number_type)

    def handle_formula(self, formula_str, get_number_type=True):
        return self._handle_formula(formula_str, get_number_type=get_number_type)


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    return x / y


def pow(x, y):
    return x ** y


def new_sum(*args):
    return sum(args)


formula_conversion_manager = FormulaConversionManager()
formula_conversion_manager.add_formula_conversion("SQRT{}", math.sqrt)
formula_conversion_manager.add_formula_conversion("SUM{}", new_sum, number_names="more")
formula_conversion_manager.add_formula_conversion("{}\^{}", pow, number_names=["x", "y"])
formula_conversion_manager.add_formula_conversion("{}/{}", divide, number_names=["x", "y"])
formula_conversion_manager.add_formula_conversion("{}\*{}", multiply, number_names=["x", "y"])
formula_conversion_manager.add_formula_conversion("{}\+{}", add, number_names=["x", "y"])
formula_conversion_manager.add_formula_conversion("{}-{}", subtract, number_names=["x", "y"])

handle_formula =  formula_conversion_manager.handle_formula
