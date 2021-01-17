# TS1-FAR-Unpack
Python-based archive unpacker for The Sims 1 FAR files

## How to use
This is essentially just a python script that reads the FAR file and extracts the contained files within.

There is a projLoc variable at the top that points towards the containing folder, and a filename variable for the file you want to open.

By default the script will just create a sub-folder using the filename, and then dump the exported files in there.
e.g. 'FileName.far' becomes a directory named 'FileName_Export\'

## Potential To-Dos
- [ ] FAR Repack (useful for large amounts of custom content & global/replacement mods)
- [ ] CLI mode for FAR Unpack
- [ ] Something to open up the extracted IFF files and view/edit data inside?

## References
FAR file format information was compiled by David Baum and Greg Noel over here: http://simtech.sourceforge.net/tech/far.html
