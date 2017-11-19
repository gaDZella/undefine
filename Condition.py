import re
from sympy.parsing.sympy_parser import (parse_expr,
                                        standard_transformations,
                                        convert_equals_signs)


def simplify(condition, keys):
    keys.update({
        "true": True,
        "false": False
    })
    patterns = {key: (r"(?<!\w)" + key + "(?!\w)") for key, value in keys.items()}
    subs = []
    new_cond = condition
    for key, p in patterns.items():
        res = re.subn(p, key, new_cond, flags=re.IGNORECASE)
        new_cond = res[0]
        subs.append(res[1])
    if max(subs + [0]) == 0:
        return condition

    transformations = standard_transformations + (convert_equals_signs,)
    condition = new_cond.replace("||", "|").replace("&&", "&").replace("!", "~").replace("==", "=")
    expr = parse_expr(condition, evaluate=False, transformations=transformations)
    if type(expr) is bool:
        return expr

    result = expr.subs(keys)
    true_expr = parse_expr("True")
    false_expr = parse_expr("False")
    if result == true_expr:
        return True
    if result == false_expr:
        return False

    return str(result).replace("|", "||").replace("&", "&&").replace("~", "!").replace("=", "==")

