#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, glob, random

## enum NetworkResults {Green, Yellow, Red, None};
LABELS = ["green", "yellow", "red", "off", "nouse"]

## use ["green", "yellow", "red", "off"] for label ('nouse" = -1)
def getlabel(path):
    idx = -1
    for lbl in LABELS[0:-1]:
        if str(path).find(lbl) != -1:
            idx = LABELS[0:-1].index(lbl)
            break
    return idx

## write lst data to csv
def write_csv(csv, dir, paths):
    for idx, path in enumerate(paths):
        lbl = getlabel(path)
        if lbl != -1:
            rpath = os.path.relpath(path, dir)
            csv.write("{}\t{}\t{}\n".format(idx, lbl, rpath))

def main():
    ## get labeled images
    dir = os.path.normpath(sys.argv[1])
    lst = sorted(glob.glob("{}/*/*".format(dir)))
    random.seed(0)
    random.shuffle(lst)
    num = len(lst)
    split = int(num * 0.8)
    train, test = lst[:split], lst[split:]

    print "NUM = {}, TRAIN = {}, TEST = {}".format(num, len(train), len(test))

    ## create train/test lst, mxnet data format
    csv_train = open("{}/train.lst".format(dir), "w")
    csv_test = open("{}/test.lst".format(dir), "w")
    write_csv(csv_train, dir, train)
    write_csv(csv_test, dir, test)
    csv_train.close()
    csv_test.close()

if __name__ == "__main__":
    main()
