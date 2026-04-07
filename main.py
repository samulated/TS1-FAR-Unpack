import os
import sys

# FAR File Format info from: http://simtech.sourceforge.net/tech/far.html

DEBUGGING = False

def debug_log(message):
    if DEBUGGING:
        print(f"DEBUG: {message}")

def parse_args(args):
    debug_log("Parsing args...")
    if len(args) <= 2:
        debug_log("Not enough arguments to proceed")
        return None
    
    output = [None, None]

    if os.path.exists(args[1]):
        debug_log("In path set")
        output[0] = args[1]
    
    if args[2] == "--here":
        output[1] = os.getcwd()
        debug_log("--here argument detected. Setting Out path to current directory")
        return output
    else:
        output[1] = args[2]
        debug_log("Out path set")
        return output

    debug_log("Args not set!")
    return None

if __name__ == '__main__':
    
    parsed_strings = parse_args(sys.argv)
    
    if parsed_strings is None:
        print("Unable to run, please ensure you run this script with an input path and either an output path or --here flag for in-place unpacking.")
        sys.exit(0)

    input_path = parsed_strings[0]
    output_path = parsed_strings[1]

    filename = input_path.split("\\")
    filename = filename[-1]

    debug_log(f"Filename set: {filename}")

    file = open(input_path, "rb")

    # header
    raw_header = file.read(16)

    header_signature = raw_header[:8].decode("utf-8")
    header_version = int.from_bytes(raw_header[8:12], 'little')
    header_manifest_offset = int.from_bytes(raw_header[12:16], 'little')

    # manifest
    file.seek(header_manifest_offset)
    manifest_header_file_number = int.from_bytes(file.read(4), 'little')

    manifest_file_length_1 = []
    manifest_file_length_2 = []
    manifest_file_offset = []
    manifest_filename_length = []
    manifest_filename = []

    i = 0
    while i < manifest_header_file_number:
        manifest_file_length_1.append(int.from_bytes(file.read(4), 'little'))
        manifest_file_length_2.append(int.from_bytes(file.read(4), 'little'))
        manifest_file_offset.append(int.from_bytes(file.read(4), 'little'))
        manifest_filename_length.append(int.from_bytes(file.read(4), 'little'))
        manifest_filename.append(file.read(manifest_filename_length[i]).decode("utf-8"))
        i += 1

    print("Manifest loaded, FAR archive contains " + str(manifest_header_file_number) + " files.")

    export_location = os.path.join(output_path, filename.split(".")[0])
    print("Default export path: " + str(export_location))

    # create export folder if doesnt exist
    if not os.path.exists(export_location):
        debug_log(f"Export folder does not exists.")
        stepped_export_location = export_location.split("\\")
        print(f"{stepped_export_location}")
        working_export_location = ""
        i = 0
        while i < len(stepped_export_location):
            working_export_location = f"{working_export_location}{stepped_export_location[i]}\\"
            debug_log(f"Checking {working_export_location}")
            if not os.path.exists(working_export_location):
                if i is 0:
                    print(f"Invalid drive specified: {working_export_location}")
                    sys.exit(0)
                else:
                    os.mkdir(working_export_location)
                    debug_log(f"Created directory: {working_export_location}")
            i += 1
    else:
        debug_log(f"Export folder is valid.")

    i = 0
    while i < manifest_header_file_number:
        working_export_location = os.path.join(export_location, manifest_filename[i])
        # if there are subfolders listed in the filename
        if "\\" in manifest_filename[i]:
            subfolders = manifest_filename[i].split("\\")
            subfolders = subfolders[:len(subfolders) - 1]
            subfolders = "\\".join(subfolders)
            # if subfolders don't exist, create directory
            if not os.path.exists(os.path.join(export_location, subfolders)):
                os.mkdir(os.path.join(export_location, subfolders))
        # write new file (if it doesn't already exist
        new_file = open(working_export_location, "wb")
        # set file reader to offset for archived file
        file.seek(manifest_file_offset[i])
        # read file to new exported file
        new_file.write(file.read(manifest_file_length_1[i]))
        new_file.close()

        i += 1
        print("Wrote file " + str(i + 1) + ": " + working_export_location)

    print("\nFiles have been successfully exported!\n")
