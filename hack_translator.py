# takes in a list, where each element is a line of parsed assembly code where:
#   element 0 = instruction type
#   element 1 = dictionary of instruction fields where:
#       a instruction fields = {"symbol":bool, "value": str}
#       c instruction fields = {"dest":str, "comp": str, "jump": str}
#       note: dest and jump are optional, if not present value = "null"
def translate_code(assembly_code):
    machine_code = []

    symbol_dict = {"R0":0,
                   "R1":1,
                   "R2":2,
                   "R3":3,
                   "R4":4,
                   "R5":5,
                   "R6":6,
                   "R7":7,
                   "R8":8,
                   "R9":9,
                  "R10":10,
                  "R11":11,
                  "R12":12,
                  "R13":13,
                  "R14":14,
                  "R15":15,
        "next_variable":16,
               "SCREEN":16384,
                  "KBD":24567,
                   "SP":0,
                  "LCL":1,
                  "ARG":2,
                 "THIS":3,
                 "THAT":4}
    
    # FIRST PASS
    instruction_number = 0
    for line_list in assembly_code:
        if line_list[0] == "label":
            label_lookup(line_list[1], instruction_number, symbol_dict)
            continue # don't add instruction number
        instruction_number += 1

    # SECOND PASS
    for line_list in assembly_code:
        op_code = ""
        full_code = ""
        instruction_type = line_list[0]
        instruction_fields = line_list[1]
        #print("instruction_type: ", instruction_type)
        #print("instruction_fields: ", instruction_fields)

        if instruction_type == "a":
            op_code = "0"
            a_command = translate_a_instruction(instruction_fields, symbol_dict)
            full_code = op_code + a_command
            #print("full a_comm: ", full_code)

        if instruction_type == "c":
            op_code = "111"
            c_command = translate_c_instruction(instruction_fields)
            full_code = op_code + c_command
            #print("full c_comm: ", full_code, " length: ", len(full_code))

        if instruction_type == "label":
            continue # second pass ignore

        #print(full_code)
        machine_code.append(full_code)

    return machine_code

def num_to_binary_as_string(num, bits):
    num = bin(num)                              # convert to binary: will have a 0b at the front
    string_num = str(num)                       # convert binary to string
    string_num = string_num[2:]                 # drop the 0b
    if len(string_num) < bits:                  # add 0's to front until byte is full
        num_0_short = bits - len(string_num)
        extra_0 = "0" * num_0_short
        string_num = extra_0 + string_num
    return string_num

def translate_a_instruction(instruction, symbol_dict):
    # 'a' instruction fields = {"symbol":bool, "value": str}
    symbol = instruction["symbol"]
    value = instruction["value"]
    if symbol:                                                  
        register_value = symbol_lookup(value, symbol_dict["next_variable"], symbol_dict)
        return register_value
    else:
        value = num_to_binary_as_string(value, 15)
        return value 

def label_lookup(label, num, symbol_dict):
    if symbol_dict.get(label) == None:
        symbol_dict[label] = num
        #return num_to_binary_as_string(num, 15)
    #else:
        #return num_to_binary_as_string(symbol_dict.get(label), 15)

def symbol_lookup(symbol, num, symbol_dict):
    if symbol_dict.get(symbol) == None:
        symbol_dict[symbol] = num
        symbol_dict["next_variable"] = num + 1
        return num_to_binary_as_string(num, 15)
    else:
        return num_to_binary_as_string(symbol_dict.get(symbol), 15)    

def translate_c_instruction(hack_c):
    comp = translate_comp(hack_c["comp"])
    dest = translate_dest(hack_c["dest"])
    jump = translate_jump(hack_c["jump"])
    result = comp + dest + jump
    return(result)

# takes in a string of the destination and returns a string of the bit values for d1 to d3
def translate_dest(dest):
    d1, d2, d3 = "0", "0", "0"
    if dest.find("A") >= 0:
        d1 = "1"
    if dest.find("D") >= 0:
        d2 = "1"
    if dest.find("M") >= 0:
        d3 = "1"
    d_code = d1 + d2 + d3
    return d_code

# takes in a string of the compute command and returns a string of the bit values for a and c1 to c6
def translate_comp(comp):
    AM = "" # truth table splits according to A or M register, use constant to fill in for either
    a = "0" # the "a" bit identifies whether the A or M register has is being addressed
    if comp.find("A") >= 0:
        AM = "A"
    if comp.find("M") >= 0:
        AM = "M"
        a = "1"
    comp_dict = {"0":"101010",
                 "1":"111111",
                "-1":"111010",
                 "D":"001100",
                  AM:"110000",
                "!D":"001101",
              "!"+AM:"110001",
                "-D":"001111",
              "-"+AM:"110011",
               "D+1":"011111",
             AM+"+1":"110111",
               "D-1":"001110",
             AM+"-1":"110010",
             "D+"+AM:"000010",
             "D-"+AM:"010011",
             AM+"-D":"000111",
             "D&"+AM:"000000",
             "D|"+AM:"010101"}

    result = ""
    for key in comp_dict:
        if comp == key:
            result = a + comp_dict[key]
            break
    return result

# takes in a string of the jump command and returns a string of the bit values for j1 to j3
def translate_jump(jump):
    if jump == "null":
        return "000"
    elif jump == "JGT":
        return "001"
    elif jump == "JEQ":
        return "010"
    elif jump == "JGE":
        return "011"
    elif jump == "JLT":
        return "100"
    elif jump == "JNE":
        return "101"
    elif jump == "JLE":
        return "110"
    else:
        return "111"