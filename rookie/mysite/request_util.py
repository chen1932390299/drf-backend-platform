import json
import re
import operator
import jsonpath
from mysite.function_plugin import hook_replace

class RequestUtil(object):

    @staticmethod
    def substitute_variable(data, const_kwargs: dict) -> dict:
        """
        @:param data of  contains ${var_name},type is dict
        @:param replace_kwargs is the replace kwargs
        @:exception: use json string to serialize  int,float,list
        """
        dump_string = json.dumps(data)
        for k, v in const_kwargs.items():
            if isinstance(v, (int, float, list)):
                ret = dump_string.replace('\"${' + str(k) + '}\"', json.dumps(v))
                dump_string = ret
            else:
                ret = dump_string.replace('${' + str(k) + '}', str(v))
                dump_string = ret
        serial = json.loads(dump_string)


        return serial

    @staticmethod
    def jsonpath_extractor(json_expr: str, body, index=0):
        """
        @:param: json path expression $..data
        @:param body the substitute body normal see like str,dict list
        @index substitute value index default is 0 ,if -1 return all value
        """
        extract_value = jsonpath.jsonpath(body, json_expr)

        if extract_value:
            if index == -1:
                return extract_value
            else:
                return extract_value[index] or None
        else:
            return None

    @staticmethod
    def regx_extractor(regx_expr, string: str, count=0):
        """
        :param regx_expr:
        :param string:
        :param count:
        :return: string
        r=re.findall(regx_expr,string)
        """
        separator_str = json.dumps(string, separators=(',', ':'))
        results = re.findall(regx_expr, separator_str)
        if results:
            return results[count]
        return None

    @staticmethod
    def assert_result(expect, actual, flag='eq'):
        """
        :param expect:
        :param actual:
        :param flag: default is eq
        :return:if  True else False
        """
        if flag == 'eq':  # a==b
            return operator.eq(expect, actual)
        if flag == "ne":  # a!=b
            return operator.ne(expect, actual)
        if flag == "lt":  # a<b
            return operator.lt(expect, actual)
        if flag == "le":  # a<=b | b contains a
            return operator.le(expect, actual)
        if flag == "gt":  # a>b
            return operator.gt(expect, actual)
        if flag == "ge":  # a>=b | a contains b
            return operator.ge(expect, actual)
        if flag == 'in':
            return True if expect in actual else False
        if flag == 'not in':
            return True if expect not in actual else False

    @staticmethod
    def get_variable(body:(dict,str,list)):
        """
        :param body:
         ??????${v}????????????
        :return: [] or ['arg1', 'arg2', 'arg3']
        """
        var_list = re.findall(r"\${([\w_]+)}", json.dumps(body, separators=(',', ':')))

        return sorted(set(var_list), key=var_list.index) or []

    @staticmethod
    def replace_str(target_str, const_kwargs):
        """
        :args??? target_str ,const_kwargs

        example:
             const_kwargs={"pwd":"xxx","var":"yyy"}
             path= "api/test?a=${pwd}&b=${var}"
             req_path=replace_str(path,const_kwargs)

        :return: api/test?a=xxx&b=yyy
        """

        var_names = re.findall(r"\${([\w_]+)}", json.dumps(target_str, separators=(',', ':')))
        for var in var_names:
            target_str = target_str.replace("${" + var + "}", const_kwargs.get(var))
        return target_str



