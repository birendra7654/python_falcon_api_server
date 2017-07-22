import sys
import getopt
import jdbe
import profiles as p
from ConfigParser import ConfigParser


def usage():
    print ("\npython load.py [OPTION...] [FILE...] [+LINE[:COLUMN]] = loads CSV profiles\n\n")
    print ("-h --help usage()")
    print ("-P --ProductProfile <ProductProfile.csv>              = loads Product Profile")

try:
    opts, args = getopt.getopt(sys.argv[1:], 'P:h', ['ProductProfile=', 'help'])
    config = ConfigParser()
    config.read('data/JDBE_local.ini')
    db = jdbe.jdbe('data/JDBE_local.ini')
    db.start()
except getopt.GetoptError:
    sys.exit(2)

for opt, arg in opts:
    try:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-P', '--ProductProfile'):
            prodfile = arg
            pfile = open(prodfile, 'rt')
            p.ProductProfile_create(db, pfile)
    except Exception as e:
        print e
