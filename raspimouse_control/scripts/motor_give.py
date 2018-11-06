#!/usr/bin/env python

import rospy

if __name__ == '__main__':
    enfile = '/dev/rtmotoren0'
    lfile = '/dev/rtmotor_raw_l0'
    rfile = '/dev/rtmotor_raw_r0'
    try:
        f = open(enfile,'w') 
        lf = open(lfile,'w')
        rf = open(rfile,'w')
        print >> f, '1'
        print >> lf, '175'
        print >> rf, '175'

        #f = open(enfile,'w') 
        #lf = open(lfile,'w')
        #rf = open(rfile,'w')
        #print >> lf, '0'
        #print >> rf, '0'
        #print >> f, '0'

        f.close()
        lf.close()
        rf.close()

    except rospy.ROSInterruptException:
        pass
