# TS1-FAR-Unpack
Python-based archive unpacker for The Sims 1 FAR files

## How to use
This is essentially just a python script that reads the FAR file and extracts the contained files within.

Use it like this:
`python main.py "C:\Some\Known\Filepath.far" "C:\An\Output\Location"`
`python main.py "C:\Some\Known\Filepath.far" --here` (for exporting to the same location that you're running the script from)

Further clean-up may be on the way in future version.

## Potential To-Dos
- [ ] FAR Repack (useful for large amounts of custom content & global/replacement mods)
- [x] CLI mode for FAR Unpack
- [ ] Something to open up the extracted IFF files and view/edit data inside?

## References
FAR file format information was compiled by David Baum and Greg Noel over here: http://simtech.sourceforge.net/tech/far.html
