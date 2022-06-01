import os
import file_handling as file
import hack_parser
import hack_translator

folder_location = os.path.dirname(os.path.realpath(__file__)) + "/"

# Provide the location of the file to run through the assembler:
assembly_file_name = 'test.txt'                 # your input assembly code file
machine_code_file_name = 'assembler_output.txt' # this will be the output file of machine code 
check_file_name = 'correct_output.txt'          # a comparison file to check output against for testing

def main():
    assembly_code = file.read_file(folder_location, assembly_file_name)            # returns a list of each line of code from input file
    assembly_code = hack_parser.parse_code(assembly_code)                          # parses the list
    machine_code = hack_translator.translate_code(assembly_code)                   # translates to binary
    file.write_list_to_file(folder_location, machine_code_file_name, machine_code) # writes to file

    # compare this assembly output with a known good one to test the assembler
    comparison = file.compare(folder_location, machine_code_file_name, check_file_name)
    print()
    print(comparison)

if __name__ == '__main__':
    main()