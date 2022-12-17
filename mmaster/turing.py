#imports

class trans:

    def __init__(self, src_state, read_symb, write_symb, tape_dir, dst_state):
        self.src_state = src_state
        self.read_symb = read_symb
        self.write_symb = write_symb
        self.tape_dir = tape_dir
        self.dst_state = dst_state
        return(None)

    def __repr__(self):
        return(f"\n\t\t{self.src_state} === \'{self.read_symb}\' / \'{self.write_symb}\' {self.tape_dir} ===> {self.dst_state}")

    def __str__(self):
        return(f"\t{self.src_state} === \'{self.read_symb}\' / \'{self.write_symb}\' {self.tape_dir} ===> {self.dst_state}")

class TM:

    # main code:

    def __init__(self, states, inputs, tapesyms, blank, leftend, trans, start, final, name = ""):
        self.states = states
        self.inputs = inputs
        self.tapesyms = tapesyms
        self.blank = blank
        self.leftend = leftend
        self.trans = trans
        self.start = start
        self.final = final
        self.name = name
        return(None)

    def __str__(self):
        return(
            f"Name:         {self.name} \n"
            f"States:       {self.states} \n"
            f"Alphabet:     \'{self.inputs}\' \n"
            f"Tape symbols: \'{self.tapesyms}\' \n"
            f"Blank:        \'{self.blank}\' \n"
            f"Leftend:      \'{self.leftend}\' \n"
            f"Transitions:  {self.trans} \n"
            f"Start state:  {self.start} \n"
            f"Final states: {self.final}"
    )

class Config:

    def __init__(self, tm, cur_state, tape_contents, head_loc):
        self.tm = tm
        self.cur_state = cur_state
        self.tape_contents = tape_contents
        self.head_loc = head_loc

        return(None)

    def __str__(self):
        return(
            f"Turing machine:           {self.tm.name} \n" 
            f"Current state:            {self.cur_state} \n"
            f"Tape contents:            {self.tape_contents} \n"
            f"Read head location:       {self.head_loc} \n" #(\'{self.tape_contents[self.head_loc]}\') \n"
    )

    def __repr__(self):
        return(
            "\n"
            f"TM: {self.tm.name}, "
            f"Current state: {self.cur_state}, "
            f"Tape contents: {''.join(self.tape_contents)}, "
            f"Read head location: {self.head_loc}, "
        )


class History:
    def __init__(self, conf_list):
        self.conf_list = conf_list
        return(None)

    def __str__(self):
        return(f"{self.conf_list}")


# Functions

# which should create a TM from this information
def createTM(states, inputs, tapesyms, blank, leftend, trans, start, final):
    return(TM(
        states=states, 
        inputs=inputs, 
        tapesyms=tapesyms, 
        blank=blank,
        leftend=leftend, 
        trans=trans, 
        start=start, 
        final=final
        ))

# which should convert a TM to a string, showing all the data of the TM in some 
# reasonably nice format
def showTM(tm_obj):
    print(tm_obj)


# which should similarly convert a Config to a string
def showConfig(conf_obj):
    print(conf_obj)

# which does the same for Historys. Please separate the elements of a History 
# by newlines when you print them, for readability.
def showHistory(hist_obj):
    print(hist_obj)

# which should take a TM and a string of input characters, and return the initial
# configuration of the machine, where the left endmarker is at very first cell of
# the tape, then the input string comes next, and the readhead points to the 
# start of the input string.
def initialConfig(tm, input):
    tape = [tm.leftend]
    for i in list(input):
        tape += i
    confg = Config(tm=tm, cur_state=tm.start, tape_contents=tape, head_loc=1)
    return(confg)

# which takes a TM, a number of steps to run the simulation, and an input string,
#  and returns the History representing running the given nondeterministic TM 
# that many steps.
def configs(tm, num_steps, input):
    hist = [initialConfig(tm, input)]

    for i in range(num_steps):
        temp_conf = hist[-1]

        try:
            head_val = temp_conf.tape_contents[temp_conf.head_loc]
        except:
            temp_conf.tape_contents += [tm.blank]
            head_val = temp_conf.tape_contents[temp_conf.head_loc]

        new_tape = temp_conf.tape_contents.copy()

        for t in tm.trans:
            if (t.src_state == temp_conf.cur_state) and (t.read_symb == head_val):
                new_state = t.dst_state
                new_tape[temp_conf.head_loc] = t.write_symb

                if t.tape_dir == 'L':
                    new_head = temp_conf.head_loc-1
                else:
                    new_head = temp_conf.head_loc+1

                break
            else:
                if t == tm.trans[-1]:
                    print("ERROR: TRANSITION NOT FOUND (in final state or does not match)")
                    return(History(hist))

        hist += [Config(tm=tm, cur_state=new_state, tape_contents=new_tape, head_loc=new_head)]

    return(History(hist))

# which takes a TM and an input string, tries to return the first Config it 
# finds whose state is a final state.
def accepting(tm, input):
    conf = initialConfig(tm, input)

    while (True):
        try:
            head_val = conf.tape_contents[conf.head_loc]
        except:
            conf.tape_contents += [tm.blank]
            head_val = conf.tape_contents[conf.head_loc]
            
        for t in tm.trans:

            if (t.src_state == conf.cur_state) and (t.read_symb == head_val):
                conf.cur_state = t.dst_state

                conf.tape_contents[conf.head_loc] = t.write_symb

                if t.tape_dir == 'L':
                    conf.head_loc -=1
                else:
                    conf.head_loc +=1

                if conf.cur_state in tm.final:
                    #print("String accepted!")
                    return(conf)

                break
            else:
                if t == tm.trans[-1]:
                    #print("String not accepted.  ")
                    return(-1)


# which takes a TM and an input string, and returns true if the TM accepts the 
# string, and false if it rejects (and may diverge, of course, if the TM diverges).
def accepts(tm, input):
    if (accepting(tm=tm, input=input) != -1):
        return(True)
    else:
        return(False)


def main():
    #print("MAIN FUNCTION: ")

    # Tests:

    # def __init__(self, src_state, read_symb, write_symb, tape_dir, dst_state):
    translist = [
        trans(1, ' ', ' ', 'R', 6),
        trans(1, '*', '*', 'R', 1),
        trans(1, 'a', '*', 'R', 2),
        trans(2, 'a', 'a', 'R', 2),
        trans(2, '*', '*', 'R', 2),
        trans(2, 'b', '*', 'R', 3),
        trans(3, 'b', 'b', 'R', 3),
        trans(3, '*', '*', 'R', 3),
        trans(3, 'c', '*', 'R', 4),
        trans(4, 'c', 'c', 'R', 4),
        trans(4, '*', '*', 'R', 4),
        trans(4, ' ', ' ', 'L', 5),
        trans(5, 'a', 'a', 'L', 5),
        trans(5, 'b', 'b', 'L', 5),
        trans(5, 'c', 'c', 'L', 5),
        trans(5, '*', '*', 'L', 5),
        trans(5, '!', '!', 'R', 1)
    ]

    #test input string:
    test_input = "aaaaabbbbbccccc"

    print(f"Example string: {test_input}, Turing machine is tripletm from MonoTMExamples.hs  ")

    # createTM (using tripletm turing machine):

    TM1 = createTM(states=[1,2,3,4,5,6], inputs="abc", tapesyms="abc* !", blank=' ', leftend='!', trans=translist, start=1, final=[6])
    TM1.name = "triplet"

    # showTM (using TM1 that was just created):
    print("showTM Test: ")
    showTM(TM1)
    print("\n\n\n")

    # showConfig and iniTialConfig:
    print("showConfig and initialConfig Test: ")
    showConfig(initialConfig(TM1, test_input))
    print("\n\n\n")

    # showHistory and configs:
    print("showHistory and configs Test: ")
    showHistory(configs(tm=TM1, num_steps=200, input=test_input))
    print("\n\n\n")    

    # accepting and accepts
    print("accepting and accepts Test: ")
    print(accepting(tm=TM1, input=test_input))
    print("\n")
    print(accepts(tm=TM1, input=test_input))
    print("\n")


    #print(f"TM1 states: {TM1.states}")

    #showTM(TM1)

    #histo = configs(TM1, 35, "aabbcc")
    #showHistory(hist_obj=histo)

    #print(accepting(TM1, "aaaaaaaabbbbbbbbcccccccc"))

if __name__ == "__main__":
    main()