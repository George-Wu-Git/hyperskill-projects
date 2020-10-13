def compare_char(regex, char):
    return regex == char or regex == '.' or not regex


def compare_eq_str(regex, string):
    if not regex or regex == "$" and not string:
        return True
    elif regex[0] == "\\":
        return compare_eq_str(regex[1:], string)
    elif len(regex) > 1 and regex[1] == "?" and string:
        return compare_eq_str(regex[2:], string) or compare_eq_str(regex[0] + regex[2:], string)
    elif len(regex) > 1 and regex[1] == "*" and string:
        return compare_eq_str(regex[2:], string) or compare_eq_str(regex, string[1:])
    elif len(regex) > 1 and regex[1] == "+" and string:
        return compare_eq_str(regex[0] + regex[2:], string) or compare_eq_str(regex, string[1:])
    elif not string or not compare_char(regex[0], string[0]):
        return False
    else:
        return compare_eq_str(regex[1:], string[1:])


def compare_str(regex, string):
    if not string and regex:
        return False
    elif compare_eq_str(regex, string):
        return True
    elif regex[0] == "^":
        return compare_eq_str(regex[1:], string)
    else:
        return compare_str(regex, string[1:])


print(compare_str(*input().split('|')))