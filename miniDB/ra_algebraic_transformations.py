
def cascade_of_s_from_two_conditions_to_consequent(dic):
    """
        σθ1∧θ2(E) = σθ1(σθ2(E))
    """

    index = dic['where'].index(' and ')
    first_condition = dic['where'][:index]
    second_condition = dic['where'][index + 5:]

    dic['where'] = first_condition

    dic['from'] = {'select': '*',
                'from': dic['from'],
                'where': second_condition,
                'distinct': None,
                'order by': None,
                'limit': None,
                'desc': None}


def cascade_of_s_from_consequent_to_two_conditions(dic):
    """
        σθ1(σθ2(E)) = σθ1∧θ2(E)
    """
    second_condition = dic['from']['where']

    dic['from'] = dic['from']['from']
    dic['where'] = dic['where'] + " and " + second_condition


def selection_operation_commutative(dic):
    """
        σθ1(σθ2(E)) = σθ2(σθ1(E))
    """

    temp_where = dic['from']['where']
    dic['from']['where'] = dic['where']
    dic['where'] = temp_where


def cascade_of_p(dic):
    """
        ΠL1(ΠL2(. . .(ΠLn(E)). . .)) = ΠL1(E)
    """

    _recursive_cascade_of_p(dic, dic)


def _recursive_cascade_of_p(dic, temp_dic):
    if not(isinstance(temp_dic['from'], dict)):
        dic['from'] = temp_dic['from']
        return

    _recursive_cascade_of_p(dic, temp_dic['from'])


def cartesian_product_to_theta_join(dic):
    """
        σθ(E1 × E2) = E1 ⊲⊳θ E2
    """
    index_of_comma = dic['from'].index(',')

    first_table = dic['from'][:index_of_comma]
    second_table = dic['from'][index_of_comma + 1:]

    dic['from'] = {'join': 'inner',
                   'left' : first_table,
                   'right' : second_table,
                   'on' : dic['where']}

    del dic['where']


def cartesian_product_to_theta_join_two_conditions(dic):
    """
    σθ1(E1 ⊲⊳σθ2 E2) = E1 ⊲⊳θ1∧θ2 E
    """

    dic['from']['on'] = dic['where'] + " and " + dic['from']['on']

    del dic['where']

def natural_join_associative(dic):
    """
        (E1 ⊲⊳ E2) ⊲⊳ E3 = E1 ⊲⊳ (E2 ⊲⊳ E3)
        here we are changing the positions of E1 and E3 (E1 ⊲⊳ E2) ⊲⊳ E3 -> (E3 ⊲⊳ E2) ⊲⊳ E1 =E1 ⊲⊳ (E2 ⊲⊳ E3)
    """

    tempLeftColumn = dic['right']['from']['left']
    dic['right']['from']['left'] = dic['left']
    dic['left'] = tempLeftColumn


def theta_join_association(dic):
    """
        (E1 ⊲⊳θ1 E2) ⊲⊳θ2∧θ3 E3 = E1 ⊲⊳θ1∧θ3(E2 ⊲⊳θ2 E3)
    """
    index = dic['on'].index(' and ')
    first_condition = dic['right']['from']['on']
    second_condition = dic['on'][:index]
    third_condition = dic['on'][index + 5:]

    dic['on'] = first_condition + " and " + third_condition

    dic['right']['from']['on'] = second_condition

    natural_join_associative(dic)
