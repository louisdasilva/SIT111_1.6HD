def read_file(location, name):
    assembly_file = open(location + name)
    assembly_code = assembly_file.readlines()
    assembly_file.close()    
    return assembly_code

def write_list_to_file(location, name, contents):
    output_file = open(location + name, "w")
    last_line = len(contents)
    count = 1
    for line in contents:
        if count < last_line:
            output_file.write(line + "\n")
        else: 
            output_file.write(line)
        count += 1
    output_file.close()

def compare(folder_location, file1, file2):
    body = read_file(folder_location, file1)
    body2 = read_file(folder_location, file2)
    
    if len(body) == len(body2):
        for line in range(0, len(body)):
            print()
            line_a = body[line].replace("\n","")
            print(line_a)
            line_b = body2[line].replace("\n","")
            print(line_b)
            if line_a == line_b:
                continue
            else:
                return "Failure at line: " + str(line + 1)
        return "Pass"
    else:
        return "Different file lengths"