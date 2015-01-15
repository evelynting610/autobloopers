from flask import Flask, request, session, g, redirect, url_for, abort, render_template

word_list = []
baked_py = ""

# creates the application
app = Flask(__name__)
#app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def read_list (text, user_word):
    global word_list
    for aline in text:                   #convert txt file to list
        if aline.startswith(user_word[0]):
            possible_words=aline.strip()
            word_list.append(possible_words)
    return word_list

def change_word(bword):
    global word_list
    wfile = open ("word_database.txt", 'r')
    read_list (wfile, bword)
    wfile.close()
    if len(bword)<4 or len(word_list)==1:
        new_word=word_list[0]
    else:
        u_end = len(bword)-1
        for i in range (0, len(word_list)):
            w_end = len(word_list[i])-1
            if bword[u_end] == word_list[i][w_end]:
                new_word=word_list[i]
                break
            else:
                new_word=word_list[1]
    word_list = []
    return new_word
    
def binary_replace (message, low, high):
    mid = int((low+high)/2)
    if (high-low)<4:
        return message
    else:
        binary_replace(message, low, mid-1)
        binary_replace(message, mid+1, high)
        message[mid]=change_word(message[mid])
    return message

@app.route('/')
def starting_page():
    return render_template('createBox.html', new_message=baked_py)

@app.route('/changemessage', methods = ['POST'])
def change_message():
    global baked_py
    baked_py=""
    user_message = request.form['Query']
    mlist=user_message.lower().split()

    end = len(mlist)-1
    if end <4:         #if it's four words or less
        mid = int(end/2)
        mlist[mid]=change_word(mlist[mid])
    else:
        mlist=binary_replace(mlist, 0, end)

    for word in mlist:
        baked_py= baked_py+word+" "
    
    return redirect('/')

if __name__ == '__main__':
    app.debug=True          #restarts every time you change code
    app.run()
