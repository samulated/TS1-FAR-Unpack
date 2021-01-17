import os
import sys

# FAR File Format info from: http://simtech.sourceforge.net/tech/far.html

# Update the below variables to match your own project area & filename
projLoc = os.path.join('D:', 'Projects', 'Modding', 'Sims 1', 'Dissect')
filename = "ExpansionPack7.far"

if __name__ == '__main__':
    file = open(os.path.join(projLoc, filename), "rb")

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

    exportLoc = os.path.join(projLoc, filename.split(".")[0] + "_Export")
    print("Default export path: " + str(exportLoc))

    # create export folder if doesnt exist
    if not os.path.exists(exportLoc):
        os.mkdir(exportLoc)

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
