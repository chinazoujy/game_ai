# -*- coding: utf-8 -*-

import math

__author__ = 'zoujinyong'

def str_replace(ss):
    return ss.replace("'", '"')

def find_nearest_tower(hero):
    pass

def judge_enemy_heros(heros, mycamp):
    '''
    获取敌方英雄分布
    :param heros:
    :param mycamp:
    :return: 占比最大的英雄种类
    '''
    pass

def get_distance(positon1, postion2):
    distance = math.sqrt(math.pow(positon1['x'] - postion2['x'], 2) + math.pow(positon1['y'] - postion2['y'], 2))
    return distance

def allocation_hero_attack_tower(heros, tower, mycamp, assigned_heros_ids):
    '''
    找到一个安全距离最近的英雄攻击指定的资源塔
    :param heros:
    :param tower:
    :return: 返回被分配的英雄ID, 无人可分配返回-1
             返回被分配英雄的下一步移动位置，无人分配返回None
    '''

    if len(assigned_heros_ids) == 5:
        return -1, None
    for hero in heros:
        if not hero['id'] in assigned_heros_ids \
                and hero['status'] != "dead" \
                and hero['camp'] == mycamp\
                and hero['status'] == "stop":
            return hero['id'], tower['position']
    return -1, None

def find_hero_by_id(heros, id):
    for hero in heros:
        if hero['id'] == id:
            return hero

def attack_tower(towers, heros, mycamp):
    commands = []
    assigned_heros_ids = [] # 已经分配的英雄IDs

    # 判断速度BUFF 塔的归属 优先获取速度塔
    for tower in towers:
        if tower['aura'] == "speed" and tower['camp'] != mycamp:
            hero_id, next_position = allocation_hero_attack_tower(heros, tower, mycamp , assigned_heros_ids)
            if hero_id == -1:
                pass
            else:
                assigned_heros_ids.append(hero_id)
                hero = find_hero_by_id(heros,hero_id)
                str_cc = {"type": "attack", "targetType": "tower",
                          "heroId": hero_id, "targetId": tower['id']}
                commands.append(str_replace(str(str_cc)))
            break

    # 其次获取双减伤塔
    for tower in towers:
        if tower['aura'] in ["magic", "physics"] and tower['camp'] != mycamp:
            hero_id, next_position = allocation_hero_attack_tower(heros, tower, mycamp , assigned_heros_ids)
            if hero_id == -1:
                pass
            else:
                assigned_heros_ids.append(hero_id)
                str_cc = {"type": "attack", "targetType": "tower",
                          "heroId": hero_id, "targetId": tower['id']}
                commands.append(str_replace(str(str_cc)))

    # 获取其他资源塔
    for tower in towers:
        if tower['camp'] != mycamp and (not tower['aura'] in ["physics", "magic", "speed"]):
            hero_id, next_position = allocation_hero_attack_tower(heros, tower, mycamp , assigned_heros_ids)
            if hero_id == -1:
                pass
            else:
                assigned_heros_ids.append(hero_id)
                str_cc = {"type": "attack", "targetType": "tower",
                          "heroId": hero_id, "targetId": tower['id']}
                commands.append(str_replace(str(str_cc)))

    return commands

def attack_hero(heros, mycamp):
    not_has_enemy_ids = []
    has_enemy_ids = []
    enemy_ids = []
    commands = []

    for i,myhero in enumerate(heros):
        if myhero['camp'] != mycamp:
            continue

        if myhero['status'] in ["dead", "attacking", "waitingAttack",]:
            continue

        for j,enemy_hero in enumerate(heros):
            if enemy_hero['camp'] == mycamp:
                continue
            distance = get_distance(myhero['position'], enemy_hero['position'])
            # 处于可攻击范围
            if myhero['status'] != "dead" and distance <= myhero["fireRange"] and myhero["fireCD"] == 0:
                str_cc = {"type": "fire", "heroId": myhero["id"], "targetId": enemy_hero["id"]}
                commands.append(str_replace(str(str_cc)))
                str_cc = {"type": "move", "heroId": myhero["id"],
                          "x": enemy_hero["position"]["x"], "y": enemy_hero["position"]["y"]}
                commands.append(str_replace(str(str_cc)))
                has_enemy_ids.append(i)
                enemy_ids.append(j)
            if myhero['status'] != "dead" and distance <= myhero["attackRange"]:
                # commands.append(str_replace(str(str_cc)))
                #
                # has_enemy_ids.append(i)
                # enemy_ids.append(j)
                pass
            else:
                not_has_enemy_ids.append(i)

    if len(not_has_enemy_ids) == 0 or len(enemy_ids) == 0:
        return commands, False

    for index in not_has_enemy_ids:
        distance = []
        for jndex in enemy_ids:
            distance.append(get_distance(heros[index]['position'], heros[jndex]['position']))
        min_index = distance.index(min(distance))
        enemy = heros[enemy_ids[min_index]]
        if heros[index]["status"] == "stop":
            str_cc = {"type": "attack", "targetType": "hero", "heroId": heros[index]["id"], "targetId": enemy["id"]}
            commands.append(str_replace(str(str_cc)))
    return commands, True

def is_attack(towers, mycamp):
    '''

    :param towers:
    :param mycamp:
    :return:
    '''
    my_towers = 0
    for tower in towers:
        if tower['camp'] == mycamp:
            my_towers += 1
    if my_towers >= 6:
        return True
    return False

def update(message):
    mycamp = message['myCamp']
    states = message['state']
    heros = states['heros']
    towers= states['towers']
    #commands = attack_tower(towers, heros, mycamp)

    if is_attack(towers, mycamp):
        commands, flag = attack_hero(heros, mycamp)
        if not flag:
            commands = attack_tower(towers, heros, mycamp)
    else:
        commands = attack_tower(towers, heros, mycamp)
    return commands

if __name__ == "__main__":
    pass