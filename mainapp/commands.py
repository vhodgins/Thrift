

## Checks if a string contains a command
from mainapp.models import Command
from mainapp import db



## Validation for command syntax is still necessary so we can catch errors

def IsCommand(standard_input):
    keywords=[
    "ATTACK", "USE","CAST","GIVE","DROP", "PICKUP", "ENDTURN", 
    "ENTER", "DESTROY", "DAMAGE", "CREATE", "CHANGESTAT", "GIVE",
    "HEAL", "RENAME", "ROLL", "CHANGESCENE", "EXEC", "BESTOW", 
    "RID", "ECHO", "RANDOMFROM", "END", "HIDE", "REVEAL",
    "STATUS", "INVENTORY", "INSPECT", "WHERE", "WHO"
    ]

    current_word = ""

    for letter in range(len(standard_input)):
        #print(standard_input[letter], end='')
        if standard_input[letter]==' ':
            if current_word in keywords:
                return True
            current_word = ''
        else:
            current_word+=standard_input[letter]
    if letter==len(standard_input)-1:
        return False

## So our method will be :
## If IsCommand(message): enqeue(message)
## and in our dequeue function, we will call Tokenize on the message, and execute it. 


# Function takes an input string and finds a command within. Commands may only be at the END of a string. 
def Tokenize(standard_input):
    keywords=[
        "ATTACK", "USE","CAST","GIVE","DROP", "PICKUP", "ENDTURN", 
        "ENTER", "DESTROY", "DAMAGE", "CREATE", "CHANGESTAT", "GIVE",
        "HEAL", "RENAME", "ROLL", "CHANGESCENE", "EXEC", "BESTOW", 
        "RID", "ECHO", "RANDOMFROM", "END", "HIDE", "REVEAL",
        "STATUS", "INVENTORY", "INSPECT", "WHERE", "WHO"
        ]

    current_word = ""

    for letter in range(len(standard_input)):
        #print(standard_input[letter], end='')
        if standard_input[letter]==' ':
            if current_word in keywords:
                break
            current_word = ''
        else:
            current_word+=standard_input[letter]
    if letter==len(standard_input)-1:
        return {'command': 'text', 'args' : None}

    si = [*standard_input]
    quoteflag=False
    for letter2 in range(len(standard_input)):
        if standard_input[letter2]=='\'':
            quoteflag = not quoteflag
        if quoteflag:
            if standard_input[letter2]==' ':
                si[letter2]='_'
        # debug output
        #print("Current letter: {cl} , Quote flag? : {qf}".format(cl=si[letter2], qf=quoteflag))

    si = ''.join(si)

    arguments = [i.strip('\'') for i in si[letter:].split(' ') if (i!=' ' and i!='')]

    #debug output

    #print("Command: {command}, Arguments: {argv}".format(command=current_word, argv=arguments))
    return {'command': current_word, 'args' : arguments}


# Queue of command objects to be fed into interpret -- Working -- 
def CommEnqueue(message, partycode):
    c = Command(comm=message, executed=False, partycode=partycode)
    db.session.add(c)
    db.session.commit()
    return None

def CommQueueLen(pc):
    return len(Command.query.filter_by(partycode=pc).all())

def CommDequeue(pc):
    comm = Command.query.filter_by(partycode=pc).first()
    commandobj = Tokenize(comm.comm)
    print(commandobj)
    Interpet(commandobj)
    db.session.delete(comm)
    db.session.commit()
    return CommQueueLen(pc)


# Function takes the command object returned by Tokenize() and executes it. 
def Interpet(command_obj):
    com = command_obj['command']
    args = command_obj['args']
    commands = '''
    if com=='ATTACK':
            ATTACK(args)
    if com=='USE':
            USE(args)
    if com=='CAST':
            CAST(args)
    if com=='GIVE':
            GIVE(args)
    if com=='DROP':
            DROP(args)
    if com=='PICKUP':
            PICKUP(args)
    if com=='ENDTURN':
            ENDTURN(args)
    if com=='ENTER':
            ENTER(args)
    if com=='DESTROY':
            DESTROY(args)
    if com=='DAMAGE':
            DAMAGE(args)
    if com=='CREATE':
            CREATE(args)
    if com=='CHANGESTAT':
            CHANGESTAT(args)
    if com=='GIVE':
            GIVE(args)
    if com=='HEAL':
            HEAL(args)
    if com=='RENAME':
            RENAME(args)
    if com=='ROLL':
            ROLL(args)
    if com=='CHANGESCENE':
            CHANGESCENE(args)
    if com=='EXEC':
            EXEC(args)
    if com=='BESTOW':
            BESTOW(args)
    if com=='RID':
            RID(args)
    if com=='ECHO':
            ECHO(args)
    if com=='RANDOMFROM':
            RANDOMFROM(args)
    if com=='END':
            END(args)
    if com=='HIDE':
            HIDE(args)
    if com=='REVEAL':
            REVEAL(args)
    if com=='STATUS':
            STATUS(args)
    if com=='INVENTORY':
            INVENTORY(args)
    if com=='INSPECT':
            INSPECT(args)
    if com=='WHERE':
            WHERE(args)
    if com=='WHO':
            WHO(args)
    '''
