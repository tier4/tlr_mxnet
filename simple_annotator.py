#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, shutil, glob
import cv2
import lst_generator

def main():
    ## get cropped images
    dir = os.path.normpath(sys.argv[1])
    lst = sorted(glob.glob("{}/raw/*".format(dir)))
    print "NUM = {}".format(len(lst))

    ## prepare labeled directories
    for lbl in lst_generator.LABELS:
        try:
            os.mkdir("{}/{}".format(dir, lbl))
        except Exception as e:
            pass

    ## annotate images with keyboard
    ## LABELS = ["green", "yellow", "red", "off", "nouse"]
    for path in lst:
        img = cv2.imread(path)
        bname = os.path.basename(path)
        cv2.imshow("What color?", img)

        dname = lst_generator.LABELS[-1]
        while True:
            key = cv2.waitKey(10)
            if key == ord("1"):
                dname = lst_generator.LABELS[0]
                break
            elif key == ord("2"):
                dname = lst_generator.LABELS[1]
                break
            elif key == ord("3"):
                dname = lst_generator.LABELS[2]
                break
            elif key == ord("4"):
                dname = lst_generator.LABELS[3]
                break
            elif key == ord(" "):
                dname = lst_generator.LABELS[-1]
                break

        src = path
        dst = "{}/{}/{}".format(dir, dname, bname)
        print "COPY: {} -> {}".format(src, dst)
        shutil.copyfile(src, dst)

    print "ALL DONE !!"

if __name__ == "__main__":
    main()
