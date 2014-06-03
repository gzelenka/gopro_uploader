#!/usr/bin/env python
import md5
import os
import os.path
import pyrax

from optparse import OptionParser


pyrax.set_setting("identity_type", "rackspace")
pyrax.set_setting("region", "DFW")
pyrax.set_credential_file("rack_auth")
cf = pyrax.cloudfiles

RAW_STASH = "MailChannelsTrexDumps"


def getopts():
    parser = OptionParser()
    parser.add_option("-n", "--name", action='store', dest='name',
                      help='name of the conatainer')
    parser.add_option("-d", "--directory", action='store_true', dest="dir",
                      default=False, help="If target is a directory")
    return parser.parse_args()


def get_md5(path):
    with open(path, 'r') as f:
        m = md5.new(f.read())

    return m.hexdigest()


if __name__ == '__main__':
    o, a = getopts()
    print o
    print a

    cont = cf.create_container(RAW_STASH)
    contents = cont.get_object_names()
    if(o.dir):
        for f in sorted(os.listdir(a[0])):
            if f not in contents:
                src = os.path.join(a[0], f)
                #print "Uploading %s/%s..." % (a[0], f)
                cf.upload_file(cont, src)
                obj = cont.get_object(f)
                if get_md5(src) != obj.etag:
                    print "UPLOAD MD5 MISMATCH!! %s" % f
                else:
                    print "%s/%s" % (cont.cdn_uri, f)

#    else:
#        cf.upload_file(cont, a[0], obj_name="FOOBAR")
