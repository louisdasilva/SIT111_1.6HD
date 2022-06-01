# takes in a list, each element is a line of code from the assembly file
# returns a list in which each element is a line of parsed assembly code where:
#   element 0 = instruction type
#   element 1 = dictionary of instruction fields where:
#       a instruction fields = {"symbol":bool, "value": int}
#       c instruction fields = {"dest":str, "comp": str, "jump": str}
def parse_code(input_assembly):
    parsed_assembly_code = []
    for line_num in range(0, len(input_assembly)):
        # traverse each line
        line = input_assembly[line_num]
        # skip empty lines or comment lines
        if line == "" or line == "\n":
            continue
        if line[0] == "/":
            continue
        # strip comments
        line = line.split("//", 1)
        line = line[0]
        # strip white spaces
        line = line.replace(" ", "")
        # strip new line symbol
        line = line.replace("\n", "")
        # break the line into instruction fields
        hack_fields = get_hack_fields(line)

        parsed_assembly_code.append(hack_fields)

    return parsed_assembly_code

# takes in a string, each string being a single line of assembly code
# returns a list, the first element is the instruction type (a,label,c) and the second element is a dictionary of the instruction fields
def get_hack_fields(line):
    
    hack_fields = []

    if(line[0] == "@"):                                         # a instructions
        hack_fields.append("a")        
        instruction = line[1:len(line)]
        hack_fields.append(process_a_instruction(instruction))    
    elif(line[0] == "("):                                       # labels
        hack_fields.append("label")
        instruction = line[1:(len(line) - 1)]
        hack_fields.append(instruction)
    else:                                                       # c instructions
        hack_fields.append("c")
        hack_fields.append(process_c_instruction(line))
    
    return hack_fields

# takes in a string, which is a hack computer 'a' instruction
# returns a dictionary of the instruction broken into fields {"symbol":bool, "value":int}
# if symbol is true the value will be -1 as the address for symbols is not yet known
# if symbol is false then "value" will contain the decimal value of the 'a' instruction
def process_a_instruction(instruction):
    # initialise dictionary for a instruction fields
    instruction_fields = {"symbol": False, 
                           "value": -1}
    
    if instruction.isdecimal():
        instruction_fields["value"] = instruction
    else:
        instruction_fields["symbol"] = True
        instruction_fields["value"] = instruction
    
    return instruction_fields

# takes in a string, which is a hack computer 'c' instruction
# returns a dictionary of the instruction broken into fields {dest,comp,jump}
def process_c_instruction(instruction):
    # dest = comp;jump ... dest and jump are optional
    instruction_fields = {"dest":"null",
                          "comp":"null",
                          "jump":"null"}
    
    has_dest = False
    has_jump = False

    comp_start = 0
    comp_finish = len(instruction)

    for character in instruction:
        if character == "=":
            has_dest = True
        if character == ";":
            has_jump = True

    if has_dest:
        comp_start = instruction.rfind("=") + 1
        instruction_fields["dest"] = instruction[0:comp_start - 1]
    if has_jump:
        comp_finish = instruction.rfind(";")
        instruction_fields["jump"] = instruction[comp_finish + 1:]

    instruction_fields["comp"] = instruction[comp_start:comp_finish]
    return instruction_fields