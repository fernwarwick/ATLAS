### PREAMBLE ###

import pandas as pd
import numpy as np
import sympy
from fractions import Fraction

# before you begin, ensure that the ATLAS html page for M is saved to the same folder,
# as is a json entitled "[group]_class_info.json"

# THINGS THAT MAY NEED EDITING WHEN USED ON DIFFERENT PAGES:
# - the order of the group
# - the relative location of the table of conjugacy classes
# - if "Conjugacy  class" and "Power  up" has an extra space
# - any file names specific to the group name

def alphanumericNumbers(string): #takes the number from the conjugacy class, eg 3B -> 3
    numberToReturn = ""
    x = list(string)
    for i in x:
        if i.isnumeric():
            numberToReturn += i
    return int(numberToReturn)

def lengthOfClass(GroupOrder,CentralizerOrders):
    OutputArray = []
    x = list(CentralizerOrders)
    for i in x:
        if str(i) != "nan":
            OutputArray.append(str(int((GroupOrder* 1/Fraction(i)))))
        else:
            OutputArray.append("-")
    return OutputArray

def CentralizerOrder(CentralizerOrder):
    OutputArray = []
    for i in CentralizerOrder:
        if str(i) != "nan":
            OutputArray.append(str(i))
        else:
            OutputArray.append("-")
    return OutputArray
        
def CentralizerShape(CentralizerOrder,Order):
    x = len(CentralizerOrder)
    OutputArray = []
    for i in range(x):
        if str(CentralizerOrder[i]) != "nan":
            if int(CentralizerOrder[i]) == int(Order[i]):
                OutputArray.append(Order[i])
            else:
                OutputArray.append("-")
        else:
            OutputArray.append("-")
    
    return OutputArray

def RationalTest(ClassName,ClassOrder,PowerUp):
    # Here ClassOrder and PowerUp are arrays
    # I am assuming that the minimum power up order is equal to or greater than that of the class order
    x = len(ClassOrder)

    OutputArray = []

    for i in range(x):
        a = str(ClassOrder[i])
        b = str(PowerUp[i])
        c = str(ClassName[i])

        if b == "nan":
            if c.find("-") == -1:
                OutputEntry = True
            else:
                OutputEntry = "-"
        else:
            OutputEntry = False
            for i in range(len(a)):
                if a[i] != b[i]:
                    OutputEntry = True

        OutputArray.append(OutputEntry)             
    return OutputArray

def RealTest(RationalInfoArray,OrderArray,PowerClassArray):
    OutputArray = []

    for i in range(len(RationalInfoArray)):
        RealTest = False
        if RationalInfoArray[i] == True:
            RealTest = True
        else:
            if RationalInfoArray[i] != "-":
                if sympy.isprime(OrderArray[i]) == True:
                    if (OrderArray[i] - 1)/(PowerClassArray[i]) % 2 == 0:
                        RealTest = True
                    else:
                        RealTest = False
                else:
                    RealTest = False
            else:
                RealTest = "-"
        
        OutputArray.append(RealTest)

    return OutputArray

def PowerUpProperForm(PowerUp):
    output = ""
    if str(PowerUp) == "nan":
        output = "-"
    else:
        x = list(str(PowerUp))
        for i in range(len(x)):
            y = ""
            if x[i].isnumeric(): # ensures a number is in proper form, eg 6A2 -> 6A^2
                if i != 0:
                    if x[i-1].isalpha():
                        y = "^"+x[i]
                    else:
                        y = x[i]
                else:
                    y = x[i]
            else:
                y = x[i]
            
            if x[i] == " ": # ensures no double spaces, eg "6A  6B" -> "6A 6B"
                if x[i-1] ==  " ":
                    y = ""
                else:
                    y = " "            
            output += y
    return output

def PowerClasses(ClassName,OrderArray,PowerUpArray):
    x = len(OrderArray)
    OutputArray = []

    for i in range(x):
        Order = str(OrderArray[i]) # Labels the order from that specific row

        if ClassName[i].find("-") != -1:
            OutputArray.append("-")

        elif PowerUpArray[i] == "-": #If the power up for that row is null, we append a 1
            OutputArray.append(1)
        
        else:
            PowerUp = str(PowerUpArray[i]).split() #split that row of the Power Up Array into an array of words
            PowerClassSum = 1 # set the number of power classes to 1

            for j in range(len(PowerUp)):   # goes through each Power Up word one by one
                PowerUpWord = PowerUp[j]    # set the individual power up word
                OrderTest = True            # assume the power up has order of the class by default

                for k in range(len(Order)):         # if the power up order is not equal to that of the class, set the test to False
                    if Order[k] != PowerUpWord[k]:
                        OrderTest = False
                
                if OrderTest == True:
                    if PowerUpWord[len(Order)].isalpha(): # add 1 to the sum if and only if the last character precedes a letter (to avoid eg class 60 counting with a class of 6) 
                        PowerClassSum += 1
                
            OutputArray.append(PowerClassSum)
    
    return OutputArray

def ClassReps(ClassRepArray): # scrapes data from the HTML table
    OutputArray = []
    for i in ClassRepArray:
        if str(i) == "nan":
            OutputArray.append("-")
        elif str(i) == "Omitted  owing to  length.":
            OutputArray.append("Omitted owing to length.")
        else:
            OutputArray.append(i)
    return OutputArray


f = open("B/ATLAS_ B.html", "r") # scrapes the ATLAS v3 page saved locally
groupOrder = 4154781481226426191177580544000000

### SCRAPING THE HTML ###
df_list = pd.read_html(f) #pandas finds the list of tables within the page
df = df_list[-2] # finds the table of conjugacy classes, which has index -2
df["Centraliser order"] = df["Centraliser order"].str.replace(" ","")
df.to_csv("B/b_atlasSite_conjugacyInfo.csv") # create a CSV for now as it's easier to work with than json


### CREATING MONSTER DF ###
class_df = pd.DataFrame() #create empty class csv


IDArr = df["Conjugacy  class"] #note the extra space, blame the scraper
LengthArr = lengthOfClass(groupOrder,df["Centraliser order"])
OrderArr = df["Conjugacy  class"].apply(alphanumericNumbers)
CentralizerOrderArr = CentralizerOrder(df["Centraliser order"])
CentralizerShapeArr = CentralizerShape(df["Centraliser order"],OrderArr)
CentralizerSmallGroupArr = "-" # BLANK
RationalArr = RationalTest(IDArr,OrderArr, df["Power  up"])
PowerUpArr = df["Power  up"].apply(PowerUpProperForm) # again, an extra space here
PowerMapArr = "-" # BLANK
PowerClassArr = PowerClasses(IDArr,OrderArr, PowerUpArr)
RealArr = RealTest(RationalArr,OrderArr,PowerClassArr)
ClassRepArr = ClassReps(df["Class  rep(s)"])



class_df["id"] = IDArr
class_df["length"] = LengthArr
class_df["order"] = OrderArr
class_df["centralizer_order"] = CentralizerOrderArr
class_df["centralizer_shape"] = CentralizerShapeArr
class_df["centralizer_small_group"] = CentralizerSmallGroupArr
class_df["rational"] = RationalArr
class_df["real"] = RealArr
class_df["power_up"] = PowerUpArr
class_df["power_map"] = PowerMapArr
class_df["power_classes"] = PowerClassArr
class_df["representative"] = ClassRepArr

class_df.to_csv("B/b_class_info.csv")
class_df.to_json("B/b_class_info_generated.json", orient="records", indent=4)

f.close

