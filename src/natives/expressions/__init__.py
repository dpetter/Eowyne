from sqlalchemy.sql.annotation import AnnotatedColumn  # @UnresolvedImport
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList, Grouping


# -------------------------------------------------------------------------------- #
def parseExpression(expression):
    '''
    Internal only. Use match(item, *criteria) instead.
    '''
    # Returns a function f(item).
    # f(item) = True exactly if the statement applies to item.
    ec = expression.__class__
    if ec == BinaryExpression:
        return compare(expression.left, expression.operator, expression.right)
    elif ec == BooleanClauseList:
        left = parseExpression(expression.clauses[0])
        right = parseExpression(expression.clauses[1])
        return lambda item: expression.operator(left(item), right(item))
    elif ec == Grouping:
        return parseExpression(expression.element)
    else:
        raise ValueError("This is not a valid search term.")

# -------------------------------------------------------------------------------- #
def compare(left, operator, right):
    '''
    Internal only. Use match(item, *criteria) instead.
    '''
    # Returns a function f(item).
    # f(item) = True exactly if the statement <left> <operator> <right> applies to
    # item.
    # <left>, <right> = either an attribute of item or a constant value.
    # <operator> = one of ==, !=, <, >, <=, >= (or more? i don't know)
    #
    # Written this way since it scales better than
    # return lambda x: operator(getValue(left), getValue(right)).
    try:
        lc = left.__class__
        rc = right.__class__
        if lc == AnnotatedColumn and rc == AnnotatedColumn:
            li = get_index(left)
            ri = get_index(right)
            return lambda item: operator(item.data[li], item.data[ri])
        elif lc == AnnotatedColumn:
            li = get_index(left)
            return lambda item: operator(item.data[li], right.value)
        elif rc == AnnotatedColumn:
            ri = get_index(right)
            return lambda item: operator(left.value, item.data[ri])
        else:
            return lambda x: operator(left.value, right.value)
    except:
        raise ValueError("This is not a valid search term.")

# -------------------------------------------------------------------------------- #
def get_index(entity):
    '''
    Internal only. Use match(item, *criteria) instead.
    '''
    fields = entity._annotations["parententity"].class_.__fields__
    return fields.index(entity.key, )