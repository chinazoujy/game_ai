# -*- coding: utf-8 -*-

__author__ = 'zoujinyong'

def move():
    pass

def str_replace(ss):
    return ss.replace("'", '"')

def find_nearest_tower(hero):
    pass

def update(ws, message):
    mycamp = message['myCamp']
    states = message['state']
    heros = states['heros']
    towers= states['towers']
    commands = []
    tower_ids = []
    for hero in heros:
        if hero['camp'] == mycamp and hero['status'] == "stop":
            for tower in towers:
                if tower['camp'] != mycamp:
                    tower_ids.append(tower['id'])
                    str_cc = {"type": "attack", "targetType": "tower",
                        "heroId": hero['id'], "targetId": tower['id']}
                    commands.append(str_replace(str(str_cc)))
    return commands

if __name__ == "__main__":
    pass