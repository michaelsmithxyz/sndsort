from sys import argv, exit
from os import makedirs
from os.path import expanduser, abspath, join, split
from subprocess import check_output
from shutil import move

VERSION="0.1"
AUTHOR="Michael Smith (s0lder)"
YEAR="2012"

def usage():
    print("snd-sort v", VERSION)
    print(AUTHOR, YEAR)
    print("Usage: snd-sort.py [dir] [file]")
    print("Description: Organizes ogg files based on attributes")
    print("Configuration:")
    print("    Per-user config files are located at ~/sndsort.conf.")
    print("    A config file is one line defining the pattern to sort with.")
    print("    Example:")
    print("        %(ARTIST)s/%(ALBUM)s/%(TITLE)s.ogg")
    print("    Tags:")
    print("        Tags are defined as such, %(TAG)s with TAG being the tag name.")
    print("        Tags are combined to form a typical Unix path.")
    print("        All OGG tags are supported, but may not always be present.")
    print("        Standard Tags:")
    print("            TITLE       - The track title")
    print("            ARTIST      - The track's artist")
    print("            ALBUM       - The track's album")
    print("            TRACKNUMBER - The track's number on the album")
    print("            DATE        - The date of release")

def getconfig(mode):
    config = open(expanduser("~/.sndsort.conf"), mode)
    return config

if __name__ == '__main__':
    try:
        config = getconfig('r')
        pattern = config.readline()
        config.close()
    except:
        print("Config not found... Creating default file...")
        pattern = "%(ARTIST)s/%(ALBUM)s/%(TRACKNUMBER)s %(TITLE)s.ogg"
        config = getconfig('w')
        config.write(pattern + '\n')
        config.close()
    if len(argv) < 2:
        usage()
        exit(1)
    if len(argv) == 2:
        outdir = argv[0]
        oggfile = argv[1]
    if len(argv) == 3:
        outdir = argv[1]
        oggfile = argv[2]
    try:
        tagtext = check_output(['vorbiscomment', oggfile])
    except:
        print("ERROR: No such OGG file:", oggfile)
        exit(1)
    tags = {}
    taglist = tagtext.decode('utf-8').split('\n')
    taglist = [x for x in taglist if x != ""]
    for tag in taglist:
        name = tag.split('=')[0]
        value = tag.split('=')[1]
        tags[name] = value
    try:
        pth = pattern % tags
    except:
        print("ERROR: Invalid tags are present")
        exit(1)
    fullpath = join(abspath(outdir), pth.strip())
    try:
        makedirs(split(fullpath)[0])
    except:
        pass
    try:
        move(oggfile, fullpath)
    except Exception as e:
        print(e)
        print("ERROR: Error moving", oggfile, "to", fullpath)
        exit(1)
