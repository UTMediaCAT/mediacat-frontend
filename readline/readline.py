DATA_PATH = '../data/current/'
with open(DATA_PATH+"interest_output.json") as myfile:
    starting_line = 47619200
    num_lines= 100
    with open("readline_output.txt","w") as output:
        for x in range(starting_line+100):
            head = next(myfile)
            if x >= starting_line:
                output.write(head)
