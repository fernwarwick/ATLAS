#####
## Check that the orders of the conjugacy class add up to the order of the group (class formula)
#####
import json
from fractions import Fraction
## Need it as "order" in the json

def ClassFormulaTest(GroupOrder,file):
    ## Input a json of conjugacy classes here vvv
    with open(file, mode = "r", encoding = "utf-8") as read_file:

        f = json.load(read_file)

    group_table = f#["classes"]

    ClassSum = 0

    for i in group_table:
            if i["length"] != "-":
                #print(Fraction(i["length"])* Fraction(i["centralizer_order"]))
                #print(i["id"], int(Fraction(i["length"]) * Fraction(i["centralizer_order"])))
                ClassSum += Fraction(i["length"])
    if int(ClassSum) == GroupOrder:
        return True
    else:
        return False
    
    return int(ClassSum)

print(ClassFormulaTest(4154781481226426191177580544000000,"B/b_class_info_generated.json"))
