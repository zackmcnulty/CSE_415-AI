import random
# Where previous remarks are stored
memory = []
previous_topics = set([])

# Where previous responses are stored
responses = []
cycle_count = 0
cycle_responses = ["And I am bored already...", \
                    "The value of this conversation is below epsilon.", \
                    "Your friends and a complete planer graph on 5 vertices must have something in common.", \
                    "Morons do exist: proof by construction.",
                    "My annoyance is monotonically increasing."] 

        

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
    global memory
    global previous_topics

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
    # CYCLE #1
    elif "i" in subs and len(subs) == 1:
        global cycle_count
        response = cycle_responses[cycle_count % 4]
        cycle_count += 1

    #
    # CYCLE #2 (Also uses memory)
    elif len(kws.intersection(previous_topics)) != 0:
        response = "hi"

    # If the other subject is not following the path of the Jedi.
    elif "fear" in remark:
        response = "Fear leads to anger, anger to hate, hate leads to suffering, suffering leads to math."

    # If you is the only subject in the remark
    elif "you" in subs and len(subs) == 1:
        response = "Don't tell me what to do. Live your own life."

    # random choice response
    else:
        response = ""
        response += random.choice(["Where", "Why", "How"])
        response += " do you "
        response += random.choice(["live with yourself", "do that", "..."])
        response += "?"

    
    memory.append(remark) 
    responses.append(response)
    previous_topics = previous_topics.union(kws)
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
