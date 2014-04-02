#!/usr/bin/env python
import os
import os.path
import pyrax

from optparse import OptionParser


pyrax.set_setting("identity_type", "rackspace")
pyrax.set_setting("region", "IAD")
pyrax.set_credential_file("rack_auth")
cf = pyrax.cloudfiles


def getopts():
    parser = OptionParser()
    parser.add_option("-n", "--name", action='store', dest='name',
                      help='name of the conatainer')
    parser.add_option("-d", "--directory", action='store_true', dest="dir",
                      default=False, help="If target is a directory")
    return parser.parse_args()


if __name__ == '__main__':
    o, a = getopts()
    print o
    print a

    cont = cf.create_container(o.name)
    if(o.dir):
        c = 1
        for f in sorted(os.listdir(a[0])):
            ext = f.split('.')[-1]
            n = "Jam%d.%s" % (c, ext)
            src = os.path.join(a[0], f)
            print "Uploading %s/%s as %s..." % (a[0], f, n)
            cf.upload_file(cont, src, obj_name=n)
            c += 1
    else:
        cf.upload_file(cont, a[0], obj_name="FOOBAR")
