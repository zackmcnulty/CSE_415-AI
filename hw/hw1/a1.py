
def five_x_cubed_plus_1(x):
    return 5*x**3 + 1

def pair_off(l):
    result = [list(x) for x in zip(l[::2], l[1::2])]
    if len(l) % 2 == 1: result.append([l[-1]])
    return result

# moves letters 19 ahead in ascii value 
def mystery_code(s):
    result = ""
    for letter in s:
        if letter.isalpha():
            if letter.isupper():
                result += chr(97 + (ord(letter) - 65 + 19) % 26)
            else:
                result += chr(65 + (ord(letter) - 97 + 19) % 26)
        else:
            result += letter

    return result


# assumed all letters are lowercase, and that all words besides special cases have >= 3 letters
def past_tense(words):
    result = []
    vowels = ["a", "e", "i", "o", "u"]
    for word in words:
        

        # handle special cases: to have, to be , to eat, to go
        if word in ["has", "have"]:
            result.append("had")
        elif word == "be":
            result.append("been")
        elif word in ["am", "is"]:
            result.append("was")
        elif word == "are":
            result.append("were")
        elif word in ["eat", "eats"]:
            result.append("ate")
        elif word in ["go", "goes"]:
            result.append("went")

        elif word[-1] == "e":
            result.append(word + "d")
        
        elif word[-1] == "y" and word[-2] not in vowels:
            result.append(word[:-1] + "ied")
        elif word[-2] in vowels and  word[-3] not in vowels and word[-1] not in (vowels + ["y", "w"]):
            result.append(word + word[-1] + "ed")
        else:
            result.append(word + "ed")

    return result

