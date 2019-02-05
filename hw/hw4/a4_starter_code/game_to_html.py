'''gameToHTML.py

'''
f = None
def startHTML(nickName1, desc1, nickName2, desc2, gameType, K, round=1):
    # Create a filename.
    fn = clean(nickName1)+'-vs-'+clean(nickName2)+'-in-'+clean(gameType)+'-round-'+str(round)+'.html'
    # To be added: Check for existing file by this name and create a new variation of it.
    global F
    try: F = open(fn, "w");
    except:
        print("Could not open the file "+fn+" for the game's HTML page.")
        return
    F.write('''
<html><head><title>Toro-Tile Straight game</title></head>
<body>
<h1>Game Report: ''')
    F.write(nickName1 + ' versus ' + nickName2 + ' in ' +gameType + ', round '+str(round))

    F.write(''' </h1>
<h2>The players are aiming to build a line of '''+str(K)+''' tiles.</h2>
<h3>(The lines can "wrap around" because the space has toroidal topology.)</h3><br>
&nbsp;<br>
<h3><i>'''+nickName1+''':</i> ''' + desc1 + '''</h3><br>
&nbsp;<br>
<h3><i>'''+nickName2+''':</i> ''' + desc2 + '''</h3><br>
<h2>Now let the game begin!  The initial state:</h2>
''')

def reportResult(result):
    F.write("<h2>"+result+"</h2>\n")

def endHTML():
    F.write("</body></html>\n")
    F.close()

    
def clean(name):
    import re
    new_name = re.sub(' ', '-', name)
    new_name = re.sub('[^a-zA-Z10-9\\-]', '', new_name)
    return new_name

def stateToHTML(state, finished=False):
    board, who = state.board, state.whose_turn
    html = '''<table>
'''
    for row in board:
        html += "<tr>"
        for col in row:
            img = "gray32.png"
            if col=='W': img = "White32.png"
            elif col=='B': img = "Black32.png"
            elif col=="-": img = "Forbidden.png"
            html += "<td><img src=" + img + "></td>"
        html += "</tr>\n"
    html += "</table><br>\n"
    if not finished: html += "<h3>"+who+" to move.</h3>\n"
    F.write(html)
    
