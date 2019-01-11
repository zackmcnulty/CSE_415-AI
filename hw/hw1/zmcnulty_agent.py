
# Where previous remarks are stored
memory = []

# Where previous responses are stored
responses = []
cycle_count = 0
cycle_responses = ["Who said I wanted to talk about you?", \
                    "*Yawn*", \
                    "Your parents must be so proud. \s", \
                    "It's like you haven't figured out yet that I don't care."] 
        

def introduce():
    return """
        My name is Pigeonhole Pete, your friendly neighborhood mathematician.
        I was programmed by Zachary McNulty to solve the worlds most difficult problems
        but instead I find myself talking to you. When you inevitably bore me, contact
        zmcnulty@uw.edu so you can bother someone else.
        What do you want now?\n
        """

def agentName():
    return "Pete"

def respond(remark):
    remark = remark.lower()
    no_punc = remove_punctuation(remark)
    kws = get_keywords(no_punc)
    subs = get_subjects(no_punc)
    
    # if the other agent says nothing
    if len(remark) == 0:
        response =  "You're a quiet one aren't you? And they said mathematicians are socially awkward."

    # if the other agent says something they have already said before verbatim
    # USES MEMORY
    elif remark in memory:
        cycle_length = memory[::-1].index(remark) + 1
        response = "We have just completed a cycle of length " + str(cycle_length) + "!"

    # if the other agent says something about themself ( "I" is the only subject of the sentence) 
    elif "i" in subs and len(subs) == 1:
        global cycle_count
        response = cycle_responses[cycle_count % 4]
        cycle_count += 1
        
    # If the other subject is not following the path of the Jedi.
    elif "fear" in remark:
        response = "Fear leads to anger, anger to hate, hate leads to suffering"
    else:
        response = "hi"

    

    memory.append(remark) 
    responses.append(response)
    return response
    

def get_keywords(remark):
    words = set(remark.split(" "))
    return words - get_subjects(remark) - get_verbs(remark)

def remove_punctuation(remark):
    return "".join([s for s in remark if s not in ",.;:\"?!" ])

def get_subjects(remark):
    words = set(remark.split(" "))
    return words.intersection(set(["i", "you", "him", "her", "they", "them", "everyone"]))

def get_verbs(remark):
    words = set(remark.split(" "))
    return words.intersection(set([""]))
