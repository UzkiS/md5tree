#!/usr/bin/python3

import sys
import os
import getopt
import hashlib

list_h = []
list_n = []
list_d = []
list_s = []
need_cmp_list = []


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", [])
        if len(args) != 2:
            raise Exception("argv error")
    except getopt.GetoptError:
        print('md5tree.py <dir_A> <dir_B>')
        sys.exit(2)
    else:
        dir_a = str(args[0])
        dir_b = str(args[1])

    def dir_diff(a_list, b_list):
        list_h = set(a_list).difference(set(b_list))
        list_n = set(b_list).difference(set(a_list))
        list_i = set(a_list).intersection(set(b_list))
        return list(list_h), list(list_n), list(list_i)

    def dir_cmp(dir_a, dir_b, dir_prefix=""):
        if dir_prefix != "":
            next_prefix = dir_prefix + "/"
        else:
            next_prefix = ""
        a_list = os.listdir(dir_a)
        b_list = os.listdir(dir_b)
        h, n, i = dir_diff(a_list, b_list)

        for x in range(len(h)):
            if dir_prefix != "":
                list_h.append(next_prefix + h[x])
            else:
                list_h.append(h[x])

        for x in range(len(n)):
            if dir_prefix != "":
                list_n.append(next_prefix + n[x])
            else:
                list_n.append(n[x])

        for x in range(len(i)):
            if os.path.isdir(dir_a + "/" + i[x]):
                dir_cmp(dir_a + "/" + i[x], dir_b +
                        "/" + i[x], next_prefix + i[x])
            else:
                if dir_prefix != "":
                    need_cmp_list.append(next_prefix + i[x])
                else:
                    need_cmp_list.append(i[x])

    dir_cmp(dir_a, dir_b)
    need_cmp_list.sort()

    for x in need_cmp_list:
        file_a = dir_a + "/" + x
        file_b = dir_b + "/" + x
        with open(file_a, 'rb') as fp:
            data_a = fp.read()
        with open(file_b, 'rb') as fp:
            data_b = fp.read()
        if hashlib.md5(data_a).hexdigest() != hashlib.md5(data_b).hexdigest():
            list_d.append(x)
        else:
            list_s.append(x)

    list_h.sort()
    list_n.sort()
    list_d.sort()
    list_s.sort()
    print("")
    print("[" + dir_a + "]")
    for x in list_h:
        print(" + " + x)
    for x in list_n:
        print(" - " + x)
    print("------------------------------")
    print("[" + dir_b + "]")
    for x in list_h:
        print(" - " + x)
    for x in list_n:
        print(" + " + x)
    print("------------------------------")
    print("Different files:")
    for x in list_d:
        print("   " + x)
    print("------------------------------")
    print("Same files:")
    for x in list_s:
        print("   " + x)
    print("")


if __name__ == "__main__":
    main(sys.argv[1:])
