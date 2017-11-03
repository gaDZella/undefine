import re
from sympy.parsing.sympy_parser import parse_expr


class Condition:

    @staticmethod
    def simplify(condition, keys):
        patterns = {key: (r"(?<!\w)" + key + "(?!\w)") for key, value in keys.items()}
        subs = []
        new_cond = condition
        for key, p in patterns.items():
            res = re.subn(p, key, new_cond, flags=re.IGNORECASE)
            new_cond = res[0]
            subs.append(res[1])
        if max(subs, default=0) == 0:
            return condition

        condition = new_cond.replace("||", "|").replace("&&", "&").replace("!", "~")
        result = parse_expr(str.format("({0}).subs({1})", condition, str(list(keys.items()))))
        true_expr = parse_expr("True")
        false_expr = parse_expr("False")
        if result == true_expr:
            return True
        if result == false_expr:
            return False
        return str(result).replace("|", "||").replace("&", "&&").replace("~", "!")

