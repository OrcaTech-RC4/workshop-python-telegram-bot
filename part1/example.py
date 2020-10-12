## WRITE CODE HERE ##

###

# simple functions
def printThis():
    print("this")

def printCustom(custom):
    print(custom)

def square(x):
    return x * x

my_dictionary = {
    "id" : 3,
    "content" : 10,
    "data" : {
        "count" : 4
    }
}

my_dictionary["extra"] = 14
key_list = list(my_dictionary.keys())
print(key_list)

#####################


n = int(input("Enter a number:"))
if n < 10:
    print("It is single-digit")
else:
    print("Whoa that's too many")

def Func(PARAM_ONE, PARAM_TWO):
    # Code: Convert to string
    RETURN_VALUE = str(PARAM_ONE) + len(str(PARAM_ONE))
    return RETURN_VALUE
