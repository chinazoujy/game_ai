# -*- coding: utf-8 -*-

__author__ = 'zoujinyong'

def test_map():
    import  json
    filename = "map.json"
    ds = json.load(open(filename, "r"))
    print type(ds)
    print len(ds)
    print len(ds[0])

if __name__ == "__main__":
    test_map()