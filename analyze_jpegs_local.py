# --------------------------------------------------------------------------
# analyze_jpegs_local.py
# Developed with Python 3.10.6 on Ubuntu Linux 22.04
#
# This extractx metadata from a local folder(s) of JPEGs and reports any which 
# have neither captions nor keywords.  There is also an option to report any 
# images which do not have BOTH a caption and keywords.
# Reqauires installation of two packages: ExifRead, and IPTCInfo3 
# (e.g., 'Sudo -H python3 -m pip install ExifRead')
# Note that IPTCInfo pops up a lot of warning messages while running, which 
# doesn't seem to affect anything.
# This program also generates a .csv file of all files' names, captions, 
# and keyword lists for further analysis if of interest.
#    - The CSV file is based on the report file name, with a .csv extensions
#
# David Young - January, 2023
# --------------------------------------------------------------------------

import os
import exifread
from iptcinfo3 import IPTCInfo
from datetime import datetime

# Start an empty exceptions report file and CSV file
photosroot = input('Enter top level folder path for photos to analyze (e.g., /home/david/Pictures): ')
exfilename = input('Enter exceptions report file path and name (e.g., /home/david/Documents/Results/excp.txt): ')
both = 'No'
both = input('Enter b or B to require BOTH captions and tags, otherwise just press Enter : ').upper()
exrpt_file = open(exfilename, 'w')
print('JPEG metadata exceptions for all files starting at root : ', photosroot, file=exrpt_file)
print('Lists non-jpegs, or where caption and/or keywords are missing', file=exrpt_file)
print('Require (B)oth captions and keywords (default = not)? - ', both, file=exrpt_file)
print('=' * 80, '\n', file=exrpt_file)
print('Started: ', datetime.now().isoformat(' ', 'seconds'), '\n', file=exrpt_file)

csvfilename = exfilename + '.csv'
csv_file = open(csvfilename, 'w')
print('"Filename","Caption","Keywords"', file=csv_file)


dircount = 0
filecount = 0
excpcount = 0
      
def analyzefile(myfilename: str):
    """Read and analyze one item from a directory list in the CWD"""
    global excpcount

    # Ignore video-type files often found in photo collections, but flag other non-JPEG's
    if ('jpg' not in myfilename.lower()) and ('jpeg' not in myfilename.lower()):  
        if (('.avi' in myfilename.lower()) or ('.mp4' in myfilename.lower()) or \
            ('.mov' in myfilename.lower())):
            return
        else:
            print(myfilename, ' - Not a JPEG', file=exrpt_file)
            excpcount += 1
            return

    # Look for EXIF captions first
    f = open(myfilename, 'rb')
    tags = exifread.process_file(f, details=False)
    if 'Image ImageDescription' in tags:
        caption = tags['Image ImageDescription']
    else:
        caption = 'None'
    f.close

    # Next look for IPTC metadata for keywords, and also for captions if none were found by EXIFRead
    iptcstuff = IPTCInfo(myfilename, force=True)

    # If exifread did not find an 'Image Description' tag, then try looking
    # for an iptc 'caption/abstract' tag
    if (caption == 'None'):
        iptccaption = iptcstuff['caption/abstract']
        if iptccaption:  # Checks to see if there was a 'caption/abstract' tag found
            caption = iptccaption

    # Get IPTC keywords; this tag pretty much always exists, even if it contains no data
    kw = iptcstuff['keywords']

    # Write out the image metadata info to the CSV file
    print('"', myfilename, '","', caption, '","', kw, '"', file=csv_file)
    
    if both == 'B':
        if ((caption == 'None') or (len(kw) == 0)):
            excpcount += 1
            print(myfilename, '- Caption: ', caption, ' - Keywords: ', kw, \
                  file=exrpt_file)
        else:
            return
    else:
        if ((caption == 'None') and (len(kw) == 0)):
            excpcount += 1
            print(myfilename, '- Caption: ', caption, ' - Keywords: ', kw, \
                  file=exrpt_file)

# end analyzefile function
        
# Main program
# Recusively walk through the top-level folder and all subfolders, and files therein in sorted order
for dirName, subdirList, fileList in os.walk(photosroot):
    dircount += 1
    print('Processing directory: %s' % dirName)
    for fname in sorted(fileList):
        filecount += 1
        fullfname = os.path.join(dirName, fname)
        analyzefile(fullfname)

# Print the report's summary statistics and show on-screen as well
print('\nDirectories : ', dircount, '\t Files : ', filecount, '\t Exceptions : ', excpcount, \
      file=exrpt_file)
print('\nEnded: ', datetime.now().isoformat(' ', 'seconds'), file=exrpt_file)
print('\nProcessing complete', file=exrpt_file)
exrpt_file.close()
csv_file.close()

print('\nDirectories : ', dircount, '\t Files : ', filecount, '\t Exceptions : ', excpcount)
print('\nProcessing complete')
