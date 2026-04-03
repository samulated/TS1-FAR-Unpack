import os
import sys

# FAR File Format info from: http://simtech.sourceforge.net/tech/far.html

# Update the below variables to match your own project area & filename
#projLoc = os.path.join('D:', 'Projects', 'Modding', 'Sims 1', 'Dissect')
#filename = "ExpansionPack7.far"

def parse_args(args):
    print("DEBUG: Parsing args...")
    if len(args) <= 2:
        print("DEBUG: Not enough arguments to proceed")
        return None
    
    out = [None, None]

    if os.path.exists(args[1]):
        print("DEBUG: In path set")
        out[0] = args[1]
    
    if args[2] == "--here":
        out[1] = os.getcwd()
        print("DEBUG: --here argument detected. Setting Out path to current directory")
        return out
    else:
        out[1] = args[2]
        print("DEBUG: Out path set")
        return out

    print("DEBUG: Args not set!")
    return None

if __name__ == '__main__':
    
    parsed = parse_args(sys.argv)
    
    if parsed is None:
        print("Unable to run, please ensure you run this script with an input path and either an output path or --here flag for in-place unpacking.")
        sys.exit(0)

    input_path = parsed[0]
    output_path = parsed[1]

    filename = input_path.split("\\")
    filename = filename[-1]

    print(f"DEBUG: Filename set: {filename}")

    file = open(input_path, "rb")

    # header
    h_raw = file.read(16)

    h_signature = h_raw[:8].decode("utf-8")
    h_version = int.from_bytes(h_raw[8:12], 'little')
    h_manifestOffset = int.from_bytes(h_raw[12:16], 'little')

    # manifest
    file.seek(h_manifestOffset)
    m_h_fileNum = int.from_bytes(file.read(4), 'little')

    m_fileLength1 = []
    m_fileLength2 = []
    m_fileOffset = []
    m_filenameLen = []
    m_filename = []

    i = 0
    while i < m_h_fileNum:
        m_fileLength1.append(int.from_bytes(file.read(4), 'little'))
        m_fileLength2.append(int.from_bytes(file.read(4), 'little'))
        m_fileOffset.append(int.from_bytes(file.read(4), 'little'))
        m_filenameLen.append(int.from_bytes(file.read(4), 'little'))
        m_filename.append(file.read(m_filenameLen[i]).decode("utf-8"))
        i += 1

    print("Manifest loaded, FAR archive contains " + str(m_h_fileNum) + " files.")

    exportLoc = os.path.join(output_path, filename.split(".")[0])
    print("Default export path: " + str(exportLoc))

    # create export folder if doesnt exist
    if not os.path.exists(exportLoc):
        print(f"DEBUG: Export folder does not exists.")
        m_exportLoc = exportLoc.split("\\")
        print(f"{m_exportLoc}")
        exportLocLong = ""
        i = 0
        while i < len(m_exportLoc):
            exportLocLong = exportLocLong + m_exportLoc[i] + "\\"
            print(f"DEBUG: Checking {exportLocLong}")
            if not os.path.exists(exportLocLong):
                if i is 0:
                    print(f"Invalid drive specified: {exportLocLong}")
                    sys.exit(0)
                else:
                    os.mkdir(exportLocLong)
                    print(f"DEBUG: Created directory: {exportLocLong}")
            i += 1
    else:
        print(f"DEBUG: Export folder is valid.")

    i = 0
    while i < m_h_fileNum:
        exportFileLong = os.path.join(exportLoc, m_filename[i])
        # if there are subfolders listed in the filename
        if "\\" in m_filename[i]:
            subfolders = m_filename[i].split("\\")
            subfolders = subfolders[:len(subfolders) - 1]
            subfolders = "\\".join(subfolders)
            # if subfolders don't exist, create directory
            if not os.path.exists(os.path.join(exportLoc, subfolders)):
                os.mkdir(os.path.join(exportLoc, subfolders))
        # write new file (if it doesn't already exist
        newFile = open(exportFileLong, "wb")
        # set file reader to offset for archived file
        file.seek(m_fileOffset[i])
        # read file to new exported file
        newFile.write(file.read(m_fileLength1[i]))
        newFile.close()

        i += 1
        print("Wrote file " + str(i + 1) + ": " + exportFileLong)

    print("\nFiles have been successfully exported!\n")
