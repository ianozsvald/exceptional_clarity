#!/usr/bin/env python """"""
from __future__ import print_function
import sys
import re

previous_traceback = None

PREPEND_STR = "<EXCEPTIONALCLARITY>"

# consider autopep8 module for checking bad syntax e.g.
# autopep8.check_syntax("if True\nprint(2)") -> False
# autopep8.check_syntax("if True:\n  print(2)") -> code object (i.e. code is
# OK)

# maybe testing for the string of the type makes more sense?
# str(type(sys.last_value)) -> "<type 'exceptions.NameError'>"

# capturing the unknown name in NameError would help in the error report

# IndentationError: doesn't come through, it looks like IPython captures it?
# SyntaxError: invalid syntax  doesn't come through either?

# To add
# use an escape fn rather than hand-escaping the rules!
# "hello" + 42
# bad imports?
# bad method name?
# missing arguments to fn?
# IndexError: list index out of range
# missing self arg in class?
# could we suggest corrected name?
# capturing sys.last_type (e.g. TypeError) and sys.last_value.args (e.g. "can
# only concatenate ...") might be saner?


# 1/0
# -> ZeroDivisionError: division by zero
PATTERN_ZERO_DIVISION = ".*ZeroDivisionError.*"
RESPONSE_ZERO_DIVISION = "ZeroDivisionErrors mean you divided by zero (e.g. 1/0), this is defined as an illegal mathematical operation. Did you really mean to divide by 0?"

# "Hello"+None
# -> TypeError: Can't convert 'NoneType' object to str implicitly
PATTERN_TYPE_ERROR = """.*TypeError\("Can't convert 'NoneType' object to (.*) implicitly.*"""
RESPONSE_TYPE_ERROR = """You did something that tries to convert None (the NoneType) into a {} and this isn't allowed.
First you probably want to understand what has type None in your expression, then consider if you're expecting that object to have a None type"""

# 'a=22; a/""'
# -> TypeError("unsupported operand type(s) for /: 'int' and 'str'",)
PATTERN_TYPE_ERROR_2_TYPES = """TypeError\("unsupported operand type\(s\) for (.*): '(.*)' and '(.*)'.*"""
RESPONSE_TYPE_ERROR_2_TYPES = """You tried to do the operation {} on two types {} and {} that don't allow that operation, are you sure you're doing something sensible?"""

# print(b)
# -> NameError: name 'b' is not defined
PATTERN_NAME_ERROR = """NameError\("name '(.*)' is not defined.*"""
RESPONSE_NAME_ERROR = "You've referenced name {} that doesn't exist in this namespace, did you mis-spell it?"

# [][0] or l=[0,1,2]; l[3]
PATTERN_LIST_INDEX_ERROR = """IndexError\('list index out of range'.*"""
RESPONSE_LIST_INDEX_ERROR = """You've indexed outside of the range of the list, use len(your_list) to get the length and index between 0 and len(your_list)-1"""

# 'TypeError("Can\'t convert \'NoneType\' object to str implicitly",)'
#PATTERN_TYPE_ERROR = """.*TypeError("Can't convert 'NoneType' object to str implicitly.*"""
#RESPONSE_TYPE_ERROR = """You did something that tries to convert None (the NoneType) into a string and this isn't allowed.
#First you probably want to understand what has type None in your expression, then consider if you're expecting that object to have a None type"""

# 'TypeError("unsupported operand type(s) for /: \'int\' and \'str\'",)'
#PATTERN_TYPE_ERROR_2_TYPES = """TypeError("unsupported operand type(s) for .*: '.*' and '.*'.*"""
#RESPONSE_TYPE_ERROR_2_TYPES = """You tried to do an operation on two types that don't allow that operation, are you sure you're doing something sensible?"""

# NameError: name 'b' is not defined
# 'NameError("name \'b\' is not defined",)'
#PATTERN_NAME_ERROR = """NameError("name '(.*)' is not defined.*"""
#RESPONSE_NAME_ERROR = "You've referenced a name (probably a variable) that doesn't exist in this namespace, did you mis-spell it?"

# patterns are sub-string matches in the error message
patterns = [(PATTERN_ZERO_DIVISION, RESPONSE_ZERO_DIVISION),
            (PATTERN_TYPE_ERROR, RESPONSE_TYPE_ERROR),
            (PATTERN_NAME_ERROR, RESPONSE_NAME_ERROR),
            (PATTERN_TYPE_ERROR_2_TYPES, RESPONSE_TYPE_ERROR_2_TYPES),
            (PATTERN_LIST_INDEX_ERROR, RESPONSE_LIST_INDEX_ERROR)
            ]
# escape the patterns
#patterns = [(escape(pattern), response) for (pattern, response) in patterns]

def print_exception_message(exc_message, items_found):
    """Print a guide to the human about the error"""
    exc_message = exc_message.format(*items_found)
    print(PREPEND_STR + ":", exc_message)


def unrecognised_exception(message):
    """We didn't recognise this exception so let the user know to file a bug"""
    print(PREPEND_STR + " This exception is NOT RECOGNISED, please file it as a bug: ", repr(message))


def parse_last_exception(message):
    """Try to match this message to our patterns to print something helpful"""
    for pattern, response in patterns:
        items_found = re.findall(pattern, repr(message))
        if items_found:
            #print("FOUND", items_found)
            print_exception_message(response, items_found[0])
            break
    else:
        unrecognised_exception(message)


def help_with_exception():
    """Callback after running an IPython command to try to help with exception messages"""
    global previous_traceback
    if 'last_traceback' in dir(sys):
        if sys.last_traceback != previous_traceback:
            previous_traceback = sys.last_traceback
            parse_last_exception(sys.last_value)


def unregister():
    """Unregister this hook if we're done with developing"""
    ip.events.unregister('post_run_cell', help_with_exception)


if __name__ == "__main__":
    print("Loaded " + PREPEND_STR + " extension")
    try:
        ip = get_ipython()
    except NameError as err:
        print(PREPEND_STR + " We couldn't execute `get_ipython()`, you have to run this from IPython")
        sys.exit()

    # http://ipython.org/ipython-doc/dev/api/generated/IPython.core.events.html
    try:
        ip.events.register("post_run_cell", help_with_exception)
    except AttributeError as err:
        print(PREPEND_STR + " Cannot register a post-run callback, maybe your version of IPython is too old?")
        print(PREPEND_STR + " Here's the raw exception message {}".format(repr(err)))
        print(PREPEND_STR + " This script has quit gracefully, it cannot be activated")
        sys.exit()

    # update last traceback if one has occurred recently
    if 'last_traceback' in dir(sys):
        previous_traceback = sys.last_traceback
