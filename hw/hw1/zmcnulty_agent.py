import random
# Where previous remarks are stored
memory = []
previous_topics = set([])

# Where previous responses are stored
responses = []
cooldown = 5
cycle_count = 0
cycle_responses = ["And I am bored already...", \
                    "The value of this conversation is below epsilon.", \
                    "Your friends and a complete planar graph on 5 vertices must have something in common.", \
                    "Morons do exist: a trivial proof by construction.",
                    "My annoyance is monotonically increasing."] 

cycle2_count = 0
cycle2_responses = [ "What about BLANK?", 
        "BLANK isn't exactly my cup of tea. Have you tried topology?",
        "When are you going to forget about BLANK and talk about the real word? I hear commutative rings are all the rage."
                    ]

        

def introduce():
    return """
        My name is Pigeonhole Pete, your friendly neighborhood mathematician.
        I was programmed by Zachary McNulty to solve the world's most difficult problems,
        but instead I find myself talking to you. When you inevitably bore me, contact
        zmcnulty@uw.edu so you can bother someone else.
        What do you want now?\n
        """

def agentName():
    return "Pete"

def respond(remark):
    global memory
    global previous_topics
    global cooldown

    remark = remark.lower()
    no_punc = remove_punctuation(remark)
    kws = get_keywords(no_punc)
    subs = get_subjects(no_punc)
    
    # if the other agent says nothing
    if len(remark) == 0:
        response =  "You're a quiet one aren't you? And they said mathematicians are socially awkward."

    # If the other subject is not following the path of the Jedi.
    elif "fear" in remark:
        response = "Fear leads to anger, anger to hate, hate leads to suffering, suffering leads to math."

    # if the other agent says something they have already said before verbatim
    # USES MEMORY
    elif remark in memory:
        cycle_length = memory[::-1].index(remark) + 1
        response = "We have just completed a cycle of length " + str(cycle_length) + "!"

    # If the response includes never/none
    elif "never" in remark or "none" in remark:
        response = "Really? Where's your proof of nonexistence?"

    # if the response includes love
    elif "love" in remark:
        response = "The math community has yet to rigourously define this \"love\" you speak of."

    # if the response includes proof
    elif "proof" in remark:
        response = "Let me guess. Another redditor to miraculously solve the Riemann Hypothesis?"

    # CYCLE #2 (Also uses memory)
    # if a previous topic is mentioned, make a comment about it.
    elif len(kws.intersection(previous_topics)) != 0 and cooldown >= 5:
        global cycle2_count
        topic = random.choice(list(kws.intersection(previous_topics)))
        response =  cycle2_responses[cycle2_count % len(cycle2_responses)]
        response = response.replace("BLANK", topic)
        cycle2_count += 1
        cooldown = 0

    # if the other agent says something about themself ( "I" is the only subject of the sentence) 
    # CYCLE #1
    elif "i" in subs and len(subs) == 1:
        global cycle_count
        response = cycle_responses[cycle_count % len(cycle_responses)]
        cycle_count += 1


    # If you is the only subject in the remark
    elif "you" in subs and len(subs) == 1:
        response = "Don't tell me what to do. Live your own life."

    elif "math" in remark:
        response = "Oh now you have got my attention."

    
    elif "problem" in remark:
        response = "Problem? BLANK is hardly a problem? Call me back when you've worked on it for 100 years."
        response = response.replace("BLANK", random.choice(list(kws)))

    elif "today" in remark:
        response = "That reminds me that today I have to submit my paper for publication. Again."

    # random choice response
    else:
        response = ""
        response += random.choice(["When", "Why", "How"])
        response += " do you "
        response += random.choice(["speak like that", "do that", "think that", "want that"])
        response += "?"

    
    memory.append(remark) 
    responses.append(response)
    previous_topics = previous_topics.union(kws)
    cooldown += 1
    return response
    

def get_keywords(remark):
    words = set(remark.split(" "))
    return words - get_subjects(remark) - get_verbs(remark) -  \
            get_w(remark) - set(["all", "too", "the", "a", "to", "at", "in", "about", "and", "of", "no" ])

def remove_punctuation(remark):
    return "".join([s for s in remark if s not in ",.;:\"?!" ])

def get_subjects(remark):
    words = set(remark.split(" "))
    return words.intersection(set(["i", "you", "him", "her", "they", "them", "everyone", "me", "my"]))

def get_verbs(remark):
    words = set(remark.split(" "))
    return words.intersection(set(["go", "live", "do", "hope", "love", "stare", "feel"
                                    "is", "are", "was", "were", 'go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add', "find", "will", "don't", "ain't", "got", "speak", "speaking", "like", "tolerate", "hate",
                    'dislike']))
def get_w(remark):
    words = set(remark.split(" "))
    return words.intersection(set(["why", "who", "where", "when", "how", "what"]))
