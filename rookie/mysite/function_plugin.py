import types
import importlib
import ast
import re
import json
import sys


def parse_string_value(str_value):
    """
    :param str_value: '123'==>123
    :return:
    """
    try:
        return ast.literal_eval(str_value)

    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


def load_module_functions(module):
    """
    load debugtalk functions mapping
    """

    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item

    return module_functions


def parse_function_params(params):
    """
    parse the function params and return it
    example:
        parse_function_params("1, 2, a=3, b=4")
    :return:  {'args': [1, 2], 'kwargs': {'a':3, 'b':4}}
    """
    function_meta = {
        "args": [],
        "kwargs": {}
    }

    params_str = params.strip()
    if params_str == "":
        return function_meta

    args_list = params_str.split(',')
    for arg in args_list:
        arg = arg.strip()
        if '=' in arg:
            key, value = arg.split('=')
            function_meta["kwargs"][key.strip()] = parse_string_value(value.strip())
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta





def extra_func_name(data):
    """
    extract method name list  of data value
    :return : ['__RandomInt(5,8)}}', '__UUID1()'] ect.
     """
    d = json.dumps(data, separators=(',', ':'))
    funcs = re.findall(r"{{(.*?)}}", d)
    return funcs


def hook_replace(data,type):
    """
    :function: replace the function with debugtalk function's return result
    :param data: {"name": "${{__RandomInt(5,8)}}", "foo2": "${{__UUID1()}}"}
    :return: dict
    :type :{0:string ,2:dict }
    """
    dump_string = json.dumps(data)
    #dynamic import
    imported_module= importlib.import_module('utils.debugtalk')
    mapping = extra_func_name(data)
    if mapping:
        for method_name in mapping:
            function_name = re.findall("(.*?)[(]", method_name)[0]
            func_mapping = load_module_functions(imported_module)
            function = func_mapping.get(function_name)
            if function:
                params = re.findall(function.__name__ + "[(](.*?)[)]", method_name)[0]
                args_kwargs = parse_function_params(params)
                args, kwargs = args_kwargs.get("args"), args_kwargs.get("kwargs")
                if not args and not kwargs:
                    res = function()
                    if isinstance(res, (int, float, list)) and type == 1:
                        ret = dump_string.replace('\"${{' + method_name + '}}\"', json.dumps(res))
                        dump_string = ret
                    else:
                        ret = dump_string.replace('${{' + method_name + '}}', str(res))

                        dump_string = ret
                else:
                    res = function(*args, **kwargs)
                    if isinstance(res, (int,float, list)) and type ==1:
                        ret = dump_string.replace('\"${{' + method_name + '}}\"', json.dumps(res))
                        dump_string = ret

                    else:
                        ret = dump_string.replace('${{' + method_name + '}}', str(res))

                        dump_string = ret
        return json.loads(dump_string)
    else:
        raise ValueError("not found ${{ }} in data ")







