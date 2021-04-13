import random
import string
import copy
import re

DIG = string.digits
LET = string.ascii_letters
SPE = '!@#$%^&*-=?_/[]()<>.'

RULE_NUM = r'.*\d.*\d.*'
RULE_UP = r'.*[A-Z].*'
RULE_LOW = r'.*[a-z].*'
RULE_SPE = r'.*[{s}].*'.format(s=SPE)

PASSWD_RULES = [
               RULE_NUM,
               RULE_UP,
               RULE_LOW
]

def password_generate(length=10, strong=False):
    rand_char = DIG + LET
    password_rule = copy.deepcopy(PASSWD_RULES)
    if strong:
        length = 17
        rand_char  += SPE
        password_rule.append(RULE_SPE)

    while True:
        password = ''.join([random.choice(rand_char) for i in range(length)])
        for rule in PASSWD_RULES:
            if not re.match(rule, password):
                break
        else:
            break
    return password