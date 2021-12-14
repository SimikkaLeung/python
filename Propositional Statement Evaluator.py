# Welcome message and instructions to use this program

print("Welcome to the Logic Evaluator program.")
print("This program accepts logical expressions following the syntax requirements:")
print("1. Each component must have a blank space in between.")
print("2. The entire expression must be inside a pair of parenthesis ().")
print("3. Each pair of parenthesis can only include maximum of 2 operands and 1 operators, as well as ")
print("   any number of complete parenthesis (). Please ensure the order of precedence is entered correctly.")
print("4. For propositional variables, you can name them using a single alphabetical letter.")
print("5. Name the variable as True if you want to enter a variable that is always true.")
print("   Similarly, name the variable as False if you want to enter a variable that is always false.")
print("6. The evaluator accepts the following logical operators: not, and, or, then, iff, xor")
print("   Example: ( ( p and q ) then r )")

# I use a while-loop here to prompt the user for input and verify if the input is correct.
# I used split() to parse the expression.
ask_for_input = True
while ask_for_input:
    expression = input("Please enter the expression following the syntax: ")
    expression = expression.lower()
    expression_breakdown = expression.split(" ")
    print("Please confirm your input is correct: ", expression_breakdown)

    if input("Yes / No: ").lower() == "yes":
        ask_for_input = False

# Declare the lists that we will use in multiple functions

propositional_variables = []   # to store only the propositional_variables
result_elements = []   # to store the results of each bracket
components = []   # to store different portions of the original expression
brackets = []     # to record the position of parenthesis in the expression
all_outcomes = []   # to record the final value of the expression of each scenario
                    # # (every unique combination of truth values assigned to the propositional_variables
exp_to_be_solved = expression_breakdown.copy()
# The exp_to_be_solved list is the list that will be manipulated by functions for evaluation.
# I use the copy() method to ensure the original expression is not affected by functions.



# This function is used for question 1. The user needs to input truth values to the propositional_variables.
# I use a while loop to ensure a truth value is wither a true or a false.
# The components list will also record the propositional_variables.

def ask_truth_values():
    global propositional_variables
    global components
    global expression_breakdown

    for element in expression_breakdown:
        if len(element) == 1 and element >= "a" and element <= "z" and not ([element, True] in propositional_variables) and not ([element, False] in propositional_variables):
            t_value = input("What is the truth value of " + element +"? True / False ")
            while len(t_value) > 0 and not ([element, True] in propositional_variables) and not ([element, False] in propositional_variables):
                if t_value.lower() == "true":
                    propositional_variables.append([element, True])
                elif t_value.lower() == "false":
                    propositional_variables.append([element, False])
                else:
                    t_value = input("What is the truth value of " + element +"? True / False ")
            components.append(element)

        elif element == "true":
            propositional_variables.append([element, True])
            components.append(element)
        elif element == "false":
            propositional_variables.append([element, False])
            components.append(element)

# This function is used for question 2. The truth values of the propositional_variables are set to true by default.
# The components list will also record the propositional_variables.
def assign_default_truth_values():
    global expression_breakdown
    global propositional_variables

    for element in expression_breakdown:
        if len(element) == 1 and element >= "a" and element <= "z" and not ([element, True] in propositional_variables):
            propositional_variables.append([element, True])
            components.append(element)
        elif element == "true":
            propositional_variables.append([element, True])
            components.append(element)
        elif element == "false":
            propositional_variables.append([element, False])
            components.append(element)


# This function flips the boolean value of a variable.
# The if statement ensures the constant TRUE and FALSE entered by the user are not changed
def change_variable_value(p_variable_index):
    if propositional_variables[p_variable_index][0] != "true" and propositional_variables[p_variable_index][0] != "false":
        propositional_variables[p_variable_index][1] = not propositional_variables[p_variable_index][1]

# This function identifies the parenthesis that has the highest order of precedence at the moment of calling
# this function, i.e. the innermost complete parenthesis counting from the left to right.
# The close parenthesis of the first complete pair is the first close parenthesis if we scan from the left to right.
# Once we have located the first close parenthesis, the closet open parenthesis on its left hand side is
# its corresponding pen parenthesis.
def search_for_parenthesis(position_open_parenthesis, position_close_parenthesis):
    pointer = 0

    # Search for the first complete parenthesis in the unsolved expression.
    while pointer <= len(exp_to_be_solved) - 1 and position_close_parenthesis == -1:
        pointer += 1
        if exp_to_be_solved[pointer-1] == ")":
            position_close_parenthesis = pointer
            index = pointer-1
            isFound = False
            while index >= 0 and position_open_parenthesis == -1 and isFound == False:
                if exp_to_be_solved[index] == "(":
                    position_open_parenthesis = index
                    isFound = True
                index -= 1

    return position_open_parenthesis, position_close_parenthesis


# This function evaluates the expression of each parenthesis identified by the function search_for_parenthesis.
# A nested-if statement is used to recognize the operator and perform the corresponding operation
# to the operands within the parenthesis. The function solve_next_parenthesis is called under some if cases
# because the right hand-side of an operator can be a parenthesis that we need to solve first.
# e.g. ( True then ( p and r ) )
# The ending part of this function reduces the exp_to_be_solved list by removing the evaluated parenthesis
# with the result of the evaluation.


def logic_evaluator(position_open_parenthesis, position_close_parenthesis):
    global exp_to_be_solved
    smallest_parenthesis = exp_to_be_solved[position_open_parenthesis + 1: position_close_parenthesis]
    index = 0
    is_operator = False
    result = True
    first_operand_value = True
    second_operand_value = True

    while not is_operator and index < len(smallest_parenthesis):
        if smallest_parenthesis[index] == "not":
            first_operand_value = get_variable_value(smallest_parenthesis[index + 1])
            result = not first_operand_value
            is_operator = True
        elif smallest_parenthesis[index] == "and":
            first_operand_value = get_variable_value(smallest_parenthesis[index - 1])
            if index == len(smallest_parenthesis) - 1:
                solve_next_parenthesis()
                second_operand_value = exp_to_be_solved[position_close_parenthesis + 1]
            else:
                second_operand_value = get_variable_value(smallest_parenthesis[index + 1])
            result = first_operand_value and second_operand_value
            is_operator = True

        elif smallest_parenthesis[index] == "or":
            first_operand_value = get_variable_value(smallest_parenthesis[index - 1])
            if index == len(smallest_parenthesis) - 1:
                solve_next_parenthesis()
                second_operand_value = exp_to_be_solved[position_close_parenthesis + 1]
            else:
                second_operand_value = get_variable_value(smallest_parenthesis[index + 1])
            if first_operand_value == True or second_operand_value == True:
                result = True
            else:
                result = False
            is_operator = True
        elif smallest_parenthesis[index] == "then":
            first_operand_value = get_variable_value(smallest_parenthesis[index - 1])
            if index == len(smallest_parenthesis) - 1:
                solve_next_parenthesis()
                second_operand_value = exp_to_be_solved[position_close_parenthesis + 1]
            else:
                second_operand_value = get_variable_value(smallest_parenthesis[index + 1])
            if second_operand_value == False and first_operand_value == True:
                result = False
            else:
                result = True
            is_operator = True
        elif smallest_parenthesis[index] == "iff":
            first_operand_value = get_variable_value(smallest_parenthesis[index - 1])
            if index == len(smallest_parenthesis) - 1:
                solve_next_parenthesis()
                second_operand_value = exp_to_be_solved[position_close_parenthesis + 1]
            else:
                second_operand_value = get_variable_value(smallest_parenthesis[index + 1])
            if first_operand_value == True and second_operand_value == True:
                result = True
            elif first_operand_value == False and second_operand_value == False:
                result = True
            else:
                result = False
            is_operator = True
        elif smallest_parenthesis[index] == "xor":
            first_operand_value = get_variable_value(smallest_parenthesis[index - 1])
            if index == len(smallest_parenthesis) - 1:
                solve_next_parenthesis()
                second_operand_value = exp_to_be_solved[position_close_parenthesis + 1]
            else:
                second_operand_value = get_variable_value(smallest_parenthesis[index + 1])
            if ( first_operand_value == False and second_operand_value == True ) or ( first_operand_value == True and second_operand_value == False ):
                result = True
            else:
                result = False
            is_operator = True
        else:
            result = exp_to_be_solved[index]
        index += 1

    # Reduce the original expression
    position = position_close_parenthesis
    while position > position_open_parenthesis:
        exp_to_be_solved.pop(position-1)
        position -= 1
    exp_to_be_solved.insert(position_open_parenthesis, result)

    result_elements.append(result)
    return result


# This function returns the corresponding, up-todate truth value og a variable.
def get_variable_value(element):
    boolean_value = False

    if element == True:
        return element
    elif element == False:
        return element
    else:
        index = 0
        isFound = False
        while index < len(propositional_variables) :
            if element == propositional_variables[index][0]:
                return propositional_variables[index][1]
            index += 1

    return boolean_value


# The function solve_next_parenthesis is called under some if cases
# because the right hand-side of an operator can be a parenthesis that we need to solve first.
# e.g. ( True then ( p and r ) )

def solve_next_parenthesis():
    parenthesis = search_for_parenthesis(-1, -1)
    position_open_parenthesis = parenthesis[0]
    position_close_parenthesis = parenthesis[1]
    logic_evaluator(position_open_parenthesis, position_close_parenthesis)


# This function checks whether we have completed the logical evaluation.
# If yes, stop the evaluation and return the final value.
# If not, continue to evaluate the remaining portions of the expression.

def continue_or_not(position_open_parenthesis, position_close_parenthesis):
    if position_open_parenthesis == -1 or position_close_parenthesis == -1:
        return
    else:
        solve_next_parenthesis()


# This function checks if we need to start the evaluation.
def start_evaluation():
    while len(exp_to_be_solved) > 1:
        continue_or_not(0, 0)

# This function is used for Question 2. It will generate 2^n unique combination of truth valuse assignements
# to n propositional variables in the original expression.
def different_combo(start, end):
    if start == end :
        start_evaluation()
        print_each_scenario()
        change_variable_value(start)
        start_evaluation()
        print_each_scenario()
        change_variable_value(start)
    if start < end :
            different_combo(start+1, end)
            change_variable_value(start)
            different_combo(start + 1, end)
            change_variable_value(start)

# This function will print a row of the truth table. I applied some formatting to the string so that
# we can see the column of the truth table clearly.
# After printing the result of one scenario, this function feeds the final value to the all_outcomes list,
# as well as clear the result_elements list and restore the exp_to_be_solved list,
# so that the two lists are ready for evaluating the next scenario.
def print_each_scenario():
    global result_elements
    global exp_to_be_solved
    global all_outcomes
    global components
    # print("print_each_scenario")

    for index1 in range(len(propositional_variables)):
        width = 9
        print("{:>{width}}".format(str(propositional_variables[index1][1]), width=width), end="\t\t")

    for index2 in range(len(components) - len(propositional_variables)):
        position = len(propositional_variables) + index2
        content = str(' '.join(components[position]))
        if len(content) <= 9:
            width = 9
        else:
            width = len(content)
        print("{:>{width}}".format(str(result_elements[index2]), width=width), end="\t\t")

    print()

    all_outcomes.append(result_elements[-1]) # Record the outcome of each scenario

    result_elements.clear()
    exp_to_be_solved = expression_breakdown.copy()


# for Question 2, the program is required to conclude whether the expression is a tautology, contradiction
# or contingency. This function counts how many final values in the all_outcome list is true to draw the conclusion.
def type_of_statement():
    global all_outcomes
    num_T = 0
    index = 0

    while index <= len(all_outcomes) - 1:
        if all_outcomes[index] == True:
            num_T += 1
        index += 1

    if num_T == len(all_outcomes):
        print("This logical expression is a tautology.")
    elif num_T == 0:
        print("This logical expression is a contradiction.")
    else:
        print("This logical expression is a contingency.")


# This function identifies the range of indexes of each portion of the logical expression.
# This allows us to display the portion as the first row of the truth table.
# Furthermore, the breakdown_brackets function will check if the number of the open parentheses is the same as the
# close parentheses in the expression. If they are not equal, the program will show an error message and
# exit the program using exit().

# To do so, the functions locates the complete brackets in a descending order of precedence,
# i.e. the complete parentheses from the innermost to the outermost, and from left to right.
# The close parenthesis of the first complete pair is the first close parenthesis if we scan from the left to right.
# Once we have located the first close parenthesis, the closet open parenthesis on its left hand side is
# its corresponding pen parenthesis.
def breakdown_brackets():

    open_brackets = []
    close_brackets = []
    global brackets
    global expression_breakdown

    index_close = 0
    while index_close <= len(expression_breakdown) - 1:
        if expression_breakdown[index_close] == ")":
            close_brackets.append(index_close)
            index_open = index_close
            move_on = False
            while index_open >= 0 and move_on == False:
                if expression_breakdown[index_open] == "(":
                    position = 0
                    not_yet_matched = True
                    while position <= len(open_brackets) - 1 and not_yet_matched:
                        if open_brackets[position] == index_open:
                            not_yet_matched = False
                        else:
                            position += 1
                    if not_yet_matched == True:
                        open_brackets.append(index_open)
                        move_on = True
                index_open -= 1
        index_close += 1

    if len(close_brackets) == expression_breakdown.count("(") and len(open_brackets) == len(close_brackets):
        for index in range(len(open_brackets)):
            brackets.append([open_brackets[index], close_brackets[index]])
    else:
        print("Error! Please restart the program and enter an expression with correct syntax.")
        exit("Please relaunch the program.")

# This function will print the the first row of the truth table, i.e. different portions of the original expression.
# I applied some formatting to the string so that we can see the column of the truth table clearly.
def print_header_truth_table():
    global brackets

    for index1 in range(len(brackets)):
        components.append(expression_breakdown[brackets[index1][0]:brackets[index1][1]+1])

    for index2 in range(len(components)):
        content = str(' '.join(components[index2]))
        if len(content) <= 9:
            width = 9
        else:
            width = len(content)
        print("{:>{width}}".format(content, width=width), end="\t\t")
    print()


# Containing functions for Question 1
def evaluate_one_condition():
    ask_truth_values()
    breakdown_brackets()
    print_header_truth_table()
    start_evaluation()
    print_each_scenario()

# Containing functions for Question 2
def truth_table ():
    assign_default_truth_values()
    breakdown_brackets()
    print_header_truth_table()
    num_variables = len(propositional_variables)
    different_combo(0, num_variables - 1)
    type_of_statement()


# The following lines of code ask the user wheher they want to excutive the application of question 1 or question 2.
# A while loop is implemented to ensure the input is correct.
question = "0"
while question != "1" and question != "2":
    print("Do you want to evaluate the propositional sentence with a truth assignment A for propositional variables (Question 1),")
    print("or to generate a truth table for the propositional sentence (Question 2)?")
    question = input("Please enter 1 or 2. ")
    if question == "1":
        evaluate_one_condition()
    elif question == "2":
        truth_table()
    else:
        print("Invalid choice.")

