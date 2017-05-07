# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

def is_regex(s):
    '''(string) -> Boolean
    checks if the given string is a valid regex or not and returns a boolean
    representing the fact. The most basic regex is define as being '1', '2',
    '0', or 'e'. There are 3 more kinds of valid regex's:
    1. r1 + '*' is also a valid regex where r1 is a valid regex
    2. '(' + r1 '|' + r2 + ')' where r1 and r2 are valid regex's
    3. '(' + r1 '.' + r2 + ')' where r1 and r2 are valid regex's

    REQ: s must be a string

    >>> is_regex('')
    'False'
    >>> is_regex('1')
    True
    >>> is_regex('2')
    True
    >>> is_regex('0')
    True
    >>> is_regex('e')
    True
    >>> is_regex('3')
    False
    >>> is_regex('2*')
    True
    >>> is_regex('2*1')
    False
    >>> is_regex('2**********')
    True
    >>> is_regex('**1')
    False
    >>> is_regex('0|1')
    False
    >>> is_regex('(0|1)')
    True
    >>> is_regex(')0|1(')
    False
    >>> is_regex('(1).')
    False
    >>> is_regex('(01)*')
    False
    >>> is_regex('((e**.(2|1)*).(1|(0.1)))')
    True
    >>> is_regex('(e*.(2|1)*).(1|(0.1))')
    False
    '''
    # a list containing the basic regex's
    basic_regex = ['0', '1', '2', 'e', '0*', '1*', '2*', 'e*']
    # a list containing both possible symbols
    symbols_regex = ['|', '.']
    # to keep track of the number of symbols in s
    sybols_count = 0
    # to keep track of the number of brackets (opened and closed) in s
    brackets_count = 0
    # counts all the symbols in string s
    sybols_count = s.count('|') + s.count('.')
    # counts all the brackets in string s
    brackets_count = s.count('(') + s.count(')')
    # if the number of brackets corresponding to the number of symbols do not
    # match, s is not a valid regex (since each symbols NEEDS 2 brackets with
    # it)
    if (sybols_count * 2) != brackets_count:
        s = False
    # if a closed bracket is found before and open bracket
    elif s.find('(') > s.find(')'):
        s = False
    # if the string is empty
    elif len(s) == 0:
        s = False
    # if the string is one of the elements in basic_regex, then this is a valid
    # regex
    elif s in basic_regex:
        s = True
    # if there is a star at the end of s, the entirety of s is valid is s[:-1]
    # (ie: s without the star) is also valid (as per rules of valid regex's)
    elif s[-1] == '*':
        # checks if everything before the * is a valid regex
        s = is_regex(s[:-1])
    # if the regex is enclosed in brackets (ie: has nested regex's)
    elif s[0] == '(' and s[-1] == ')':
        # need to see if the sub regex's are also valid
        s = sub_regexs(s)
    # other wise s is false
    else:
        s = False

    # return whether s is valid or not
    return s


def sub_regexs(s):
    '''(string) -> boolean

    This function checks the sub regex's within s are valid using indirect
    recursion with is_regex() (ie: a regex ((0|1).(1|2)) well need its inner
    parts to be evaluated as valid if the whole is to be evaluated as a
    valid regex). If NO open and closing brackets are found at the end and
    beginning of s, False will be returned regardless of whether s is a valid
    regex or not (non bracket cases are taken care of in is_regex())

    REQ: s must be a string

     >>> sub_regexs('(0|1)')
    True
    >>> sub_regexs('((0|1).(1|2))')
    True
    >>> sub_regexs('(0.1).1')
    False
    >>> sub_regexs('((0.1).1)')
    True
    >>> sub_regexs('((e**.(2|1)*).(1|(0.1)))')
    True
    >>> sub_regexs('(e*.(2|1)*).(1|(0.1))')
    False
    >>> sub_regexs('1')
    False
    >>> sub_regexs('2')
    False
    >>> sub_regexs('0')
    False
    >>> sub_regexs('e')
    False
    >>> sub_regexs('1*')
    False
    '''
    try:
        # uses a helper function to find the main operator of s (not of the
        # sub regexs)
        index_symbol = find_operator(s)[1]
        # getting the left side of the main symbol operator
        left_regex = s[1:index_symbol]
        # getting the right side of the main symbol operator
        right_regex = s[index_symbol + 1:-1]

        # checking whether both the left and right sub regexs from the main
        # operator are valid regexs
        validity = is_regex(left_regex) and is_regex(right_regex)
    except:
        # if any errors occur (due to invalid regexs being entered)
        validity = False

    return validity


def all_regex_permutations(s):
    '''(string) -> set of strings

    This function takes in an string and outputs a set containing all
    permutations of s that are valid regex expressions. Valid regex expressions
    consist of:
    1. r1 + '*' is also a valid regex where r1 is a valid regex
    2. '(' + r1 '|' + r2 + ')' where r1 and r2 are valid regex's
    3. '(' + r1 '.' + r2 + ')' where r1 and r2 are valid regex's
    4. '0' or '1' or '2' or 'e'
    Length of s must be less that 15 or else, the program will crash due to
    lack of sufficient memory.

    REQ: s must be a string
    REQ: s < 12

    >>> all_regex_permutations('sfsdfds34234())09')
    set()
    >>> all_regex_permutations('(1|0)')
    {'(0|1)', '(1|0)'}
    >>> all_regex_permutations('1')
    {'1'}
    >>> all_regex_permutations('(1*.(1|0))')
    {'((1*.1)|0)', '(0*|(1.1))', '(0.(1|1*))', '(1.(0*|1))', '(1|(1*.0))',
    '(1|(1.0*))', '((0.1)*|1)', '(1|(1.0)*)', '(0|(1*.1))', '(0.(1*|1))',
    '((1.1*)|0)', '(1|(0.1))*', '((0|1)*.1)', '(1.(1|0))*', '((0.1)|1*)',
    '((1.1)*|0)', '((1*|1).0)', '((1*|0).1)', '((0|1).1)*', '(1.(0|1)*)',
    '(1.(0|1))*', '((0|1*).1)', '((0|1).1*)', '(1*.(0|1))', '(1.(1|0*))',
    '(1|(0.1)*)', '((1*.0)|1)', '((1|1)*.0)', '(0|(1.1)*)', '((1|1).0)*',
    '(0*.(1|1))', '((0*.1)|1)', '(1*|(1.0))', '(1|(0*.1))', '(1|(1.0))*',
    '((1|0).1)*', '(1*|(0.1))', '((1.0*)|1)', '(1.(1*|0))', '((1|0).1*)',
    '((1.1)|0*)', '((1|1*).0)', '((0.1*)|1)', '(0.(1|1))*', '((1.0)|1*)',
    '((1.0)|1)*', '((0.1)|1)*', '(0|(1.1*))', '((1|0*).1)', '((1.1)|0)*',
    '((1.0)*|1)', '(1|(0.1*))', '(1.(1|0)*)', '(0.(1|1)*)', '(1*.(1|0))',
    '((1|1).0*)', '((0*|1).1)', '(1.(0|1*))', '((1|0)*.1)', '(0|(1.1))*'}
    '''
    # a list containing the basic regex's
    basic_regex = ['0', '1', '2', 'e']
    # a list containing both possible symbols
    symbols_regex = ['|', '.', '*', '(', ')']
    # used to check if the expression is invalid or not
    invalid = False
    # checks each character of s
    for char in s:
        # checks if the current char is not a valid regex character (outlined
        # in basic_regex and symbols_regex)
        if char not in basic_regex and char not in symbols_regex:
            # empty list because there are not valid string
            actual = []
            invalid = True
    if not(invalid):
        # finds all possible permutations of s
        permutations = get_combinations(list(s))
        # a list to represent all valid regexs
        actual = []
        # runs for each permutations
        for i in range(len(permutations)):
            # if the current permutation is a regex
            if is_regex(permutations[i]):
                # append it to the list
                actual.append(permutations[i])
    # return the set of all valid expressions
    return set(actual)


def get_combinations(s):
    '''(string) -> list of string
    This function takes in a string and returns a set of all permutations of
    it, including itself (a permutation is a just a rearrangement of the same
    number/kind of letter to create a new word). If s is 1 character long then
    s will be returned (not a list). This will not cause any issues with the
    other functions

    REQ: s must be a string

    >>> get_combinations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    >>> get_combinations('a')
    'a'
    >>> get_combinations('')
    []
    '''
    # base case
    if len(s) <= 1:
        # if s is empty then there are no permutations (NOT usd as a base case
        # for the recursive call)
        if len(s) == 0:
            combos = []
        # if the s has 1 charater then the only possible combo is itself
        # this is used as a base case for the recursive call
        else:
            combos = s
    else:
        # a list to store the possible combinations in
        combos = []
        # runs for each letter in s
        for i in range(len(s)):
            # the current char to be looked at
            current_char = s[i]
            # the rest of s excluding the one being currently looked at
            rest_chars = s[:i] + s[i+1:]
            # the recursive step, where permutations is a string combination
            # that will be added to the current char to create a new
            # permutation.
            for permutations in get_combinations(rest_chars):
                # incase tbe user enters a string with a space
                if current_char is not '':
                    # the new combination
                    new_combo = current_char + permutations
                else:
                    new_combo = permutations
                # adding the combo to the list of combinations(combos)
                combos.append(new_combo)
    # returning the combinations
    return combos


def regex_match(r, s):
    '''(RegexTree, string) -> boolean

    Returns whether or not s is a matching string to the given RegexTree
    (rooted at r). Returns True if it matches. Rules for matching:
    1.  (regex matches to string)'0' matches to '0', '1' matches to '1',
        '2' matches to '2','e' matches to ''
    2. A regex in the form r + '*' matches to: 1. an empty string('')
                                               2. s if s has the for s1+s2+s3..
                                                where r matches to all si
    3. A regex in the form '(' + r1 + '|' + 'r2' + ')' matches to s if r1
        matches to s or r2 matches to s or both
    4. A regex in the form '(' + r1 + '|' + 'r2' + ')' matches to s is the
        concatination os s1 and s2 (s = s1 + s2) and r1 matches s1 and r2
        matches s2

    REQ: r must be a valid RegexTree
    REQ: s must be a string

    >>> regex_match(StarTree(Leaf('1')), '111111111111111111111111111111')
    True
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), '')
    True
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), '010110100101010')
    True
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), '0102001010')
    False
    >>> regex_match(BarTree(DotTree(Leaf('0'), Leaf('1')), DotTree(Leaf('1'),
    StarTree(Leaf('e')))), '01')
    True
    >>> regex_match(BarTree(DotTree(Leaf('0'), Leaf('1')), DotTree(Leaf('1'),
    StarTree(Leaf('e')))), '1')
    True
    >>> regex_match(BarTree(DotTree(Leaf('0'), Leaf('1')), DotTree(Leaf('1'),
    StarTree(Leaf('e')))), '1eeeeeeeee')
    False
    '''
    # Base case; r is a leaf (ie: has no children)
    if r.get_children() == []:
        # if the leaf's sybmol is an 'e' (which matches too '')
        if r.get_symbol() == 'e':
            # if s is a empty string
            matches = ('' == s)
        else:
            # checking is the symbol of the r matches to s (ie: 1 matches to 1)
            matches = (r.get_symbol() == s)
    else:
        # getting the current symbol
        symbol = r.get_symbol()
        if symbol == '.':
            # default boolean value
            matches = False
            # this loop is used to try to find an s1 and an s2 such that
            # s1 + s2 match to r and r1 matches to s1; r2 matches to s2
            for i in range(len(s)):
                if matches is False:
                    # this try catch is implemented to avoid any indexing
                    # errors (s2 being an empty string and the very end of the
                    # string)
                    try:
                        # if the left child is a Star tree
                        if (len(s) == 1 and
                                r.get_children()[0].get_symbol() == '*'):
                            # if s is 1 and the left child is a Star tree then
                            # s1 MUST be '' and s2 MUST be s
                            matches = (regex_match(r.get_children()[0], '') and
                                       regex_match(r.get_children()[1], s))
                        # elif the right child is a Star tree
                        elif (len(s) == 1 and
                                r.get_children()[1].get_symbol() == '*'):
                            # if s is 1 and the right child is a Star tree then
                            # s1 MUST be s and s2 MUST be ''
                            matches = (regex_match(r.get_children()[0], s) and
                                       regex_match(r.get_children()[1], ''))
                        else:
                            # check if certain slicing's of s with the left
                            # and right subtrees match to make s1 and s2. If
                            # s1 and s2 are found such that matches is True
                            # then the loop is stopped
                            matches = (regex_match(
                                r.get_children()[0], s[:i]) and
                                       regex_match(
                                           r.get_children()[1], s[i:]))
                    except:
                        # checking if s1 is s and s2 is '' (ie: got the end of
                        # the list and matches was stil false)
                        matches = (regex_match(r.get_children()[0], s) and
                                   regex_match(r.get_children()[1], ''))
        # if the symbol is a bar
        elif symbol == '|':
            # do a recursive call on the left and right children using an or
            # statement (as per definition 3). If any one of the children match
            # s, then then this too matches s
            matches = regex_match(r.get_children()[0], s) or regex_match(
                r.get_children()[1], s)
        # if the symbol is a star
        elif symbol == '*':
            # a list containing the operators
            symbol_regex = ['|', '.']
            # a list containing the basic regex's
            basic_regex = ['0', '1', '2', 'e']
            # if s is empty (is a valid matching string to '*' as per
            # definition 2)
            if s == '':
                matches = True
            # if the next symbol is a bar
            elif r.get_child().get_symbol() == symbol_regex[0]:
                # default boolean; used in an initial comparison
                matches = True
                # checks each character of s
                for base in s:
                    # makes sure each character in s is a valid regex
                    # (since the '*' operator indicates a repetition or
                    # characters or an empty string)
                    matches = matches and regex_match(r.get_child(), base)
            # if there are no sub regex's (operators) in the current root
            else:
                # finding pattern of repitition
                repitition = repitition_finder(s)
                # check if the child of start matches the pattern of repitition
                matches = regex_match(r.get_child(), repitition)
        # if the symbol is a dot
        else:
            # if non of these cases apply then the tree rooted at r does not
            # match
            matches = False

    return matches


def repitition_finder(regex):
    '''(string) -> string
    This function takes in a string, regex and determines which part of the
    string is the repeating pattern. If no pattern is found then the original
    regex will be returned

    REQ: regex must be a string

    >>> repitition_finder('abcabcabc')
    'abc'
    >>> repitition_finder('0110001110101011000111010101100011101010110001110101
    01100011101010110001110101')
    '0110001110101'
    >>> repitition_finder('abcxyz')
    'abcxyz'
    >>> repitition_finder('')
    ''
    '''
    # a var for the pattern of repition
    pattern = ''
    # used to see if a repeating pattern has been found
    repitition_found = False
    # runs for each character in regex
    for base in regex:
        if repitition_found is False:
            # adding a new character to the possible pattern
            pattern += base
            # runs for the length of regex
            for i in range(-1, len(regex)):
                # in this part check if pattern can be turned into the original
                # regex if so, the we have found the repitition pattner
                if (pattern * (i + 1)) == regex:
                    repitition_found = True
    # returning the pattern of repitions
    return pattern


def build_regex_tree(regex):
    '''(string) -> RegexTree

    This function takes in a VALID regextree string and returns the root of the
    corresponding regex tree and its root.

    REQ: regex must be a valid regex

    >>> build_regex_tree('1')
    Leaf('1')
    >>> build_regex_tree('(0|1)')
    BarTree(Leaf('0'), Leaf('1'))
    >>> build_regex_tree('(1.e)')
    DotTree(Leaf('1'), Leaf('e'))
    >>> build_regex_tree('(1*.e)')
    DotTree(StarTree(Leaf('1')), Leaf('e'))
    >>> tree = build_regex_tree('((0.1)|(1|e*))')
    >>> tree == BarTree(DotTree(Leaf('0'), Leaf('1')), BarTree(Leaf('1'),
    StarTree(Leaf('e'))))
    True
    >>> tree = build_regex_tree('((e**.(2|1)*).(1|(0.1)))')
    >>> tree == DotTree(DotTree(StarTree(StarTree(Leaf('e'))),
    StarTree(BarTree(Leaf('2'), Leaf('1')))), BarTree(Leaf('1'),
    DotTree(Leaf('0'), Leaf('1'))))
    True
    >>> tree = build_regex_tree('2************')
    >>> tree == StarTree(StarTree(StarTree(StarTree(StarTree(StarTree(
    StarTree(StarTree(StarTree(StarTree(StarTree(StarTree(Leaf('2')))))))))))))
    True
    '''
    # the basic regex's
    basic_regex = ['0', '1', '2', 'e']

    # base case; if the regex is a basic regex then create a Leaf object for it
    if regex in basic_regex:
        # creating the new leave
        new_node = Leaf(regex)

    else:
        # getting the main operator ('|' , '.', or '*') and its index
        info = find_operator_build_tree(regex)
        # account for a special case like ((1.2).(1|0))*
        if (regex[-1] == '*' and ((regex.count('.') + regex.count('|')) > 1)):
            info = ['*', len(regex) - 1]
        # seperating and assingning the info
        operator, index = info[0], info[1]
        # if the current operator is a dot
        if operator == '.':
            # create a DotTree with its left and right children
            # being regex trees if everthing before and after the operator
            # LEFT CHILD = everything before the operator
            # RIGHT CHILD = evereything after the operator
            new_node = DotTree(build_regex_tree(
                regex[1:index]), build_regex_tree(regex[index + 1:-1]))
        # if the current operator is a bar
        elif operator == '|':
            # create a BarTree with its left and right children
            # being regex trees if everthing before and after the operator
            new_node = BarTree(build_regex_tree(
                regex[1:index]), build_regex_tree(regex[index + 1:-1]))
        # if the current operator is a star
        elif operator == '*':
            # creat a StarTree and have its chilren be a regex tree of
            # everything before the operator
            regex = regex[:regex.rfind('*')]
            new_node = StarTree(build_regex_tree(regex))
    # returning the root
    return new_node


def find_operator(regex):
    ''' (string) -> list(string, index)

    This function  takes in a string regex, finds the main operator acting
    within it. Valid operators can either be '|', '*' or '.'. If there is no
    valid operator found (ie: this function does however return the correct
    values for some invalid regex's but that won't affect other code/output),
    then an index of -1 and an operator '*' is provided (if an index of -1 is
    given then the false '*' returned won't matter). This version of
    find_operator gives priority to the operators '|' and '.' over '*'
    (to certain cases outlined in the examples below)

    REQ: regex must be a string

    >>> find_operator('')
    [*, -1]
    >>> find_operator('1')
    ['*', -1]
    >>> find_operator('1*')
    ['*', 1]
    >>> find_operator('(e|1)')
    ['|', 2]
    >>> find_operator('(e|1).')
    ['*', -1]
    >>> find_operator('((0|1).1)')
    ['.', 6]
    >>> find_operator('(1*.(0|1).1)')
    ['.', 9]
    >>> find_operator('((e**.(2|1)*).(1|(0.1)))')
    ['.', 13]
    >>> find_operator('(((e**.(2|1)*).(1|(0.1)))|((2***|0).(0*1*)****))')
    ['|', 25]
    >>> find_operator('(0.1)*')
    ['.', 2] # The type of case that DIFFERS from find_operator_build_tree
    >>> find_operator('((0.1).(1|0))*')
    ['.', 6]



    '''
    # the 2 main symbols that are being looked for
    symbols_regex = ['|', '.']
    # keeps track of all Open brackets
    bracketO = []
    # keeps track of all Closed brackets
    bracketC = []
    # so pop() is not done in the beggining (if bracketO is empty)
    first = False
    # only runs if there are open AND closed brackets
    if '(' in regex and ')' in regex:
        # if there are no inner brackets in regex, then the operator
        # can be found (the outer brackets are ignored for this)
        if not('(' in regex[1:-1]) and not(')' in regex[1:-1]):
            # checking if a certaain symbol is in regex
            if symbols_regex[0] in regex[1:-1]:
                operator = '|'
                index = regex.find('|')
            else:
                operator = '.'
                index = regex.find('.')
        else:
            for i in range(1, len(regex[1:-1])):
                # if an Open bracket is found as position i, it is appended
                # to bracketO
                if regex[i] == '(':
                    bracketO.append('(')
                # if a closed bracket it found
                elif regex[i] == ')':
                    # if this is not the very first iteration
                    if first:
                        # pops the open bracket from bracketO if a closed
                        # bracket is found
                        bracketO.pop()
                # if there are no more brackets found in bracketO
                # signals that the loop is no long inside of the sub regex
                # (left or right child)
                if len(bracketO) == 0:
                    # if '*', '(' and ')' are not found in the regex
                    if (not(regex[i] == '*') and
                            not(regex[i] == '(') and not(regex[i] == ')')):
                        # if any of the valid operators are in the regex after
                        # the last closed bracket
                        if (symbols_regex[0] in regex[i:] or
                                symbols_regex[1] in regex[i:]):
                            # saves the index
                            index = i
                            # saves the operator
                            operator = regex[i]
                # if the first iteration is done
                first = True
            # if none of the operators are in regex, and the loop has reached
            # the end, then a '*' is returned
            if not(operator in symbols_regex):
                operator = '*'
                index = regex.rfind('*')
    else:
        # if there are not brackets present('2*')
        operator = '*'
        index = regex.find('*')
    # returning the data as a list
    return [operator, index]


def find_operator_build_tree(regex):
    ''' (string) -> list(string, index)

    This function  takes in a string regex, finds the main operator acting
    within it. Valid operators can either be '|', '*' or '.'. If there is no
    valid operator found (ie: this function does however return the correct
    values for some invalid regex's but that won't affect other code/output),
    then an index of -1 and an operator '*' is provided (if an index of -1 is
    given then the false '*' returned won't matter). This version of
    find_operator does not give priority to any symbol

    REQ: regex must be a string

    >>> find_operator_build_tree('')
    [*, -1]
    >>> find_operator_build_tree('1')
    ['*', -1]
    >>> find_operator_build_tree('1*')
    ['*', 1]
    >>> find_operator_build_tree('(e|1)')
    ['|', 2]
    >>> find_operator_build_tree('(e|1).')
    ['*', -1]
    >>> find_operator_build_tree('((0|1).1)')
    ['.', 6]
    >>> find_operator_build_tree('(1*.(0|1).1)')
    ['.', 9]
    >>> find_operator_build_tree('((e**.(2|1)*).(1|(0.1)))')
    ['.', 13]
    >>> find_operator_build_tree('(((e**.(2|1)*).(1|(0.1)))|((2***|0).(
    0*1*)****))')
    ['|', 25]
    >>> find_operator_build_tree('(0.1)*')
    ['*', 5] # The type of case that DIFFERS from find_operator
    >>> find_operator_build_tree('((0.1).(1|0))*')
    ['.', 6]
    '''
    # the 2 main symbols that are being looked for
    symbols_regex = ['|', '.']
    # keeps track of all Open brackets
    bracketO = []
    # keeps track of all Closed brackets
    bracketC = []
    # so pop() is not done in the beggining (if bracketO is empty)
    first = False
    # only runs if there are open AND closed brackets
    if '(' in regex and ')' in regex:
        # if there are no inner brackets in regex, then the operator
        # can be found (the outer brackets are ignored for this)
        if not('(' in regex[1:-1]) and not(')' in regex[1:-1]):
            # checking if a certaain symbol is in regex
            if symbols_regex[0] in regex[1:-1]:
                operator = '|'
                index = regex.find('|')
            else:
                operator = '.'
                index = regex.find('.')
        else:
            for i in range(1, len(regex[1:-1])):
                # if an Open bracket is found as position i, it is appended
                # to bracketO
                if regex[i] == '(':
                    bracketO.append('(')
                # if a closed bracket it found
                elif regex[i] == ')':
                    # if this is not the very first iteration
                    if first:
                        # pops the open bracket from bracketO if a closed
                        # bracket is found
                        bracketO.pop()
                # if there are no more brackets found in bracketO
                # signals that the loop is no long inside of the sub regex
                # (left or right child)
                if len(bracketO) == 0:
                    # if '*', '(' and ')' are not found in the regex
                    if (not(regex[i] == '*') and
                            not(regex[i] == '(') and not(regex[i] == ')')):
                        # saving the index
                        index = i
                        # saving the operator
                        operator = regex[i]
                # if the first iteration is done
                first = True
            # if none of the operators are in regex, and the loop has reached
            # the end, then a '*' is returned
            if not(operator in symbols_regex):
                operator = '*'
                # r find is done to find the right most '*' (ie: '2*****')
                index = regex.rfind('*')
    else:
        # if there are not brackets present('2*')
        operator = '*'
        index = regex.find('*')
    # returning the data as a list
    return [operator, index]
