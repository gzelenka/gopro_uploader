#!/usr/bin/env python
import md5
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


def get_md5(path):
    with open(path, 'r') as f:
        m = md5.new(f.read())

    return m.hexdigest()


if __name__ == '__main__':
    o, a = getopts()
    print o
    print a

    cont = cf.create_container("NeedTranscode")
    if(o.dir):
        c = 1
        for f in sorted(os.listdir(a[0])):
            ext = f.split('.')[-1]
            n = "Jam%d.%s" % (c, ext)
            src = os.path.join(a[0], f)
            print "Uploading %s/%s as %s..." % (a[0], f, n)
            meta = {'finished_container_name': o.name,
                   }
            cf.upload_file(cont, src, obj_name=n,
                                  content_type="video/H264")
            obj = cont.get_object(n)
            if get_md5(src) != obj.etag:
                print "UPLOAD MD5 MISMATCH!!"
            else:
                print "md5 verified"

            obj.set_metadata(meta)
            c += 1
#    else:
#        cf.upload_file(cont, a[0], obj_name="FOOBAR")
