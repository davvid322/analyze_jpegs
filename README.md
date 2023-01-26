# analyze_jpegs
These programs analyze jpeg files in a folder and all subfolders in order
to detect any which do not have captions and/or keywords in their metadata
### Usage Notes
- There are two versions of the program.  One accesses a local folder / directory,
and the other accesses a network folder connected via a Samba share.
- The Samba version doesn't like network server names.  You need to instead use the 
IP address of the server followed by the share name (e.g., 192.168.0.50/Pictures Master).
- The programs generate an exceptions report text file, as well as a .csv file
containing all of the captions / keywords found for each file analyzed.
- This is a plain text program that runs in a terminal.
