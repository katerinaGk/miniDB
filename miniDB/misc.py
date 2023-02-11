import operator

def get_op(op, a, b):
    '''
    Get op as a function of a and b by using a symbol
    '''
    ops = {'>': operator.gt,
                '<': operator.lt,
                '>=': operator.ge,
                '<=': operator.le,
                '=': operator.eq,
                #OPERATOR FOR THE NOT CONDITION
                'not':operator.ne,
                #OPERATOR FOR THE BETWEEN CONDITION
                'between':between
                }

    try:
        return ops[op](a,b)
    except TypeError:  # if a or b is None (deleted record), python3 raises typerror
        return False

def split_condition(condition):
    ops = {'>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq,
           '>': operator.gt,
           '<': operator.lt,
           #OPERATOR FOR THE NOT CONDITION
           'not':operator.ne,
           #OPERATOR FOR THE BETWEEN CONDITION
           'between':between
           }

    for op_key in ops.keys():
        splt=condition.split(op_key)
        if len(splt)>1:
            left, right = splt[0].strip(), splt[1].strip()
            if(op_key=='between'):
                right=right.replace(' ','')
            if right[0] == '"' == right[-1]: # If the value has leading and trailing quotes, remove them.
                right = right.strip('"')
            elif ' ' in right: # If it has whitespaces but no leading and trailing double quotes, throw.
                raise ValueError(f'Invalid condition: {condition}\nValue must be enclosed in double quotation marks to include whitespaces.')

            if right.find('"') != -1: # If there are any double quotes in the value, throw. (Notice we've already removed the leading and trailing ones)
                raise ValueError(f'Invalid condition: {condition}\nDouble quotation marks are not allowed inside values.')

            return left, op_key, right

def reverse_op(op):
    '''
    Reverse the operator given
    '''
    return {
        '>' : '<',
        '>=' : '<=',
        '<' : '>',
        '<=' : '>=',
        '=' : '='
    }.get(op)


#FUNCTION USED IN BETWEEN FEATURE
def between(v,condition):
    condition=condition.replace('and',' ')
    condition=condition.split()
    if(condition[0].isnumeric()):
        #FOR NUMERICAL CHECKS
        low=float(condition[0])
        high=float(condition[1])
        v=float(v)
        if(v>low and v<high):
            return True
        else:
            return False
    else:
        #FOR STRING CHECKS
        if(v>condition[0] and v<condition[1]):
            return True
        else:
            return False