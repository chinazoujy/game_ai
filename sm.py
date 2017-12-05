# -*- coding: UTF-8 -*-

import math

MAX_TOWERS_COUNT = 4
LOW_BLOOD_TOWERS = 0
FULL_TOWERS_COUNT = 6

TOWER_LOW_BLOOD = 90

FULL_TIME = 3*60*1000 # ms
DEARTH_TIME = (2*60+37)*1000
LAST_TIME = (2*60+58)*1000

def str_replace(ss):
    return ss.replace("'", '"')

def cmd_attack(heroId, targetType, targetId):
    str_cc = {"type": "attack", "targetType": targetType,
              "heroId": heroId, "targetId": targetId}
    return str_replace(str(str_cc))

def cmd_fire(heroId, targetId):
    str_cc = {"type": "fire", "heroId": heroId, "targetId": targetId}
    return str_replace(str(str_cc))

def cmd_move(heroId, x, y):
    str_cc = {"type": "move", "heroId": heroId, "x": x, "y": y}
    return str_replace(str(str_cc))

def cmd_stop(heroId):
    str_cc = {"type": "stop", "heroId": heroId}
    return str_replace(str(str_cc))

def get_distance(positon1, postion2):
    return math.sqrt(math.pow(positon1['x'] - postion2['x'], 2) + math.pow(positon1['y'] - postion2['y'], 2))

def check_mycamp_tower(towers, mycamp):
    '''
    检查本方的防御塔是否在遭到攻击
    遭到攻击条件为：1.敌方英雄下达了攻击指令
    :param towers:
    :param mycamp:
    :return:
    '''
    pass

def find_neareat_enemy_tower(hero_positon, towers, mycamp, assigned_tower):
    print "assigned_tower ", assigned_tower
    nearest_tower_id = -1
    min_distance = 1e10
    for tower in towers:
        if tower["healthPoint"] < TOWER_LOW_BLOOD:
            continue
        if tower["camp"] == mycamp:
            continue
        if tower["id"] in assigned_tower:
            continue
        distance = get_distance(tower["position"], hero_positon)
        if distance < min_distance:
            min_distance = distance
            nearest_tower_id = tower["id"]
    if nearest_tower_id != -1:
        assigned_tower.append(nearest_tower_id)
    return nearest_tower_id

def find_nearest_enemy_hero(current_hero_position, heros, mycamp):
    nearest_hero_id = -1
    min_distance = 1e10
    for hero in heros:
        if hero["camp"] == mycamp:
            continue
        if hero["status"] == "dead":
            continue
        distance = get_distance(hero["position"], current_hero_position)
        if distance < min_distance:
            min_distance = distance
            nearest_hero_id = hero["id"]
    return nearest_hero_id

def find_nearest_enemy_hero_in_kill_model(current_hero_position, heros, mycamp, assigned_hero):
    nearest_hero_id = -1
    min_distance = 1e10
    enemy_dazing_heros = []
    for hero in heros:
        if hero["camp"] == mycamp:
            continue
        if hero["status"] == "dead":
            continue
        # if hero["id"] in assigned_hero:
        #     continue
        distance = get_distance(hero["position"], current_hero_position)
        if distance < min_distance:
            min_distance = distance
            nearest_hero_id = hero["id"]
    # if nearest_hero_id != -1:
    #     assigned_hero.append(nearest_hero_id)
    return nearest_hero_id


def find_max_distance_teammate(hero_position, heros, mycamp):
    nearest_teammate_id = -1
    max_distance = 0
    for h in heros:
        if h["camp"] != mycamp:
            continue
        if h["status"] == "dead":
            continue
        distance = get_distance(h["position"], hero_position)
        if distance > max_distance:
            max_distance = distance
            nearest_teammate_id = h["id"]
    return nearest_teammate_id

def find_hero_by_id(id, heros):
    for hero in heros:
        if hero["id"] == id:
            return hero

def find_tower_by_id(id, towers):
    for tower in towers:
        if tower["id"] == id:
            return tower

def escape(current_hero, heros, towers, mycamp, camps, game_time, assigned_tower):
    """
     英雄逃跑时，攻击敌方资源塔->移动到最近队友的位置->随机位置移动
    :param current_hero:
    :param heros:
    :param towers:
    :param mycamp:
    :return:
    """
    nearest_tower_id = find_neareat_enemy_tower(current_hero["position"], towers, mycamp, assigned_tower)
    if nearest_tower_id == -1:
        nearest_teammate_id = find_max_distance_teammate(current_hero["position"], heros, mycamp)
        if nearest_teammate_id == -1:
            #UNDO random escape
            return None
        else:
            hero = find_hero_by_id(nearest_teammate_id, heros)
            return cmd_move(nearest_teammate_id, hero["position"]["x"], hero["position"]["y"])
    else:
        return cmd_attack(current_hero["id"], "tower", nearest_tower_id)


def stop(current_hero, heros, towers, mycamp, camps, game_time, assigned_tower):
    """
    英雄停止时，攻击防御塔-> 攻击最近的敌人
    :param current_hero:
    :param heros:
    :param towers:
    :param mycamp:
    :return:
    """
    nearest_tower_id = find_neareat_enemy_tower(current_hero["position"], towers, mycamp, assigned_tower)
    if nearest_tower_id != -1:
        return cmd_attack(current_hero["id"], "tower", nearest_tower_id)
    else:
        nearest_enemy_hero_id = find_nearest_enemy_hero(current_hero["position"], heros, mycamp)
        if nearest_enemy_hero_id != -1:
            return cmd_attack(current_hero["id"], "hero", nearest_enemy_hero_id)
        else:
            return None

def attack_tower(current_hero, heros, towers, mycamp, camps, game_time, assigned_tower):
    """
    英雄在攻击防御塔时，
    :return:

    """
    nearest_enemy_hero_id = find_nearest_enemy_hero(current_hero["position"], heros, mycamp)
    if nearest_enemy_hero_id != -1:
        enemy_hero = find_hero_by_id(nearest_enemy_hero_id, heros)
        distance = get_distance(current_hero["position"], enemy_hero["position"])
        if distance <= current_hero["fireRange"]:
            return cmd_attack(current_hero["id"], "hero", nearest_enemy_hero_id)
        else:
            tower_id = current_hero["executingCmd"]["targetId"]
            tower = find_tower_by_id(tower_id, towers)
            #if tower["healthPoint"] <= TOWER_LOW_BLOOD and tower["aura"] not in ["physics", "magic"]:
            if tower["healthPoint"] <= TOWER_LOW_BLOOD:
                return cmd_stop(current_hero["id"])
            else:
                return None
    else:
        tower_id = current_hero["executingCmd"]["targetId"]
        tower = find_tower_by_id(tower_id, towers)
        if tower["healthPoint"] < TOWER_LOW_BLOOD:
            return cmd_stop(current_hero["id"])
        else:
            return None

def moving(current_hero, heros, towers, mycamp, camps, game_time, assigned_tower):
    """
    英雄在移动时，如果当前防御塔数目大于等于 MAX_TOWERS_COUNT 则扫描周围距离并对处于攻击范围的敌人进攻 否则不做处理
    :param current_hero:
    :param heros:
    :param mycamp:
    :param camps:
    :return:
    """
    cmd = current_hero["cmd"]
    if cmd["targetType"] == "tower":
        tower_id = cmd["targetId"]
        tower = find_tower_by_id(tower_id, towers)
        if tower["healthPoint"] <= TOWER_LOW_BLOOD:
            return cmd_stop(current_hero["id"])

    nearest_enemy_hero_id = find_nearest_enemy_hero(current_hero["position"], heros, mycamp)
    if nearest_enemy_hero_id != -1:
        enemy_hero = find_hero_by_id(nearest_enemy_hero_id, heros)
        distance = get_distance(current_hero["position"], enemy_hero["position"])
        if distance <= current_hero["fireRange"]:
            return cmd_attack(current_hero["id"], "hero", nearest_enemy_hero_id)
        else:
            return None
    else:
        return None



def attack_hero(current_hero, heros, towers, mycamp, camps, game_time, assigned_tower):
    """
    英雄在攻击过程中，检查当前的防御塔数量占有量，当大于等于MAX_TOWERS_COUNT时，检查技能CD 否则 转而攻击防御塔
    :param current_hero:
    :param towers:
    :param mycamp:
    :param camps:
    :return:
    """
    executingCmd = current_hero["executingCmd"]
    if current_hero["fireCD"] == 0:
        return cmd_fire(current_hero["id"], executingCmd["targetId"])
    else:
        if executingCmd["type"] == "fire":
            return cmd_attack(current_hero["id"], "hero", executingCmd["targetId"])
        else:
            return None

def death(current_hero, heros, towers, mycamp, camps, game_time,assigned_tower):
    return None

def unattacked(current_hero, heros, towers, mycamp, camps,game_time, assigned_tower):
    if camps[mycamp]["towerCount"] >= MAX_TOWERS_COUNT:
        nearest_id = find_nearest_enemy_hero(current_hero["position"], heros, mycamp)
        if nearest_id != -1:
            executingCmd = current_hero["executingCmd"]
            if executingCmd is None or len(executingCmd) == 0:
                return cmd_attack(current_hero["id"], "hero", nearest_id)
            else:
                return None
        else:
            return None
    else:
        executingCmd = current_hero["executingCmd"]
        if executingCmd is None or len(executingCmd) == 0:
            nearest_tower_id = find_neareat_enemy_tower(current_hero["position"], towers, mycamp, assigned_tower)
            if nearest_tower_id == -1:
                return None
            else:
                return cmd_attack(current_hero["id"], "tower", nearest_tower_id)
        else:
            return None

def check_state(hero):
    if hero['status'] == "dead":
        return "death"
    elif hero["status"] == "dazing":
        return "unattacked"
    elif hero["status"] == "moving":
        return "move"
    elif hero["status"] in ["firing", "waitingFire"]:
        return "attack_hero"
    elif hero["status"] in ["attacking", "waitingAttack"]:
        if hero["executingCmd"]["targetType"] == "tower":
            return "attack_tower"
        else:
            return "attack_hero"
    elif hero["status"] == "stop":
        return "stop"
    else:
        print "CHECK ERROR"
        print hero["status"]
        return None

switch = {
            "escape": escape,
            "stop": stop,
            "attack_tower": attack_tower,
            "move": moving,
            "attack_hero": attack_hero,
            "death": death,
            "unattacked": unattacked
        }

def find_neareat_enemy_tower_in_kill_model(hero_positon, towers, mycamp):
    nearest_tower_id = -1
    min_distance = 1e10
    for tower in towers:
        if tower["camp"] == mycamp:
            continue

        distance = get_distance(tower["position"], hero_positon)
        if distance < min_distance:
            min_distance = distance
            nearest_tower_id = tower["id"]
    return nearest_tower_id

def kill(current_hero, heros, towers, mycamp, assigned_hero):
    cmd = current_hero["cmd"]
    executingCmd = current_hero["executingCmd"]

    if current_hero["status"] == "stop":
        nearest_enemy_id = find_nearest_enemy_hero_in_kill_model(current_hero["position"], heros, mycamp, assigned_hero)
        if nearest_enemy_id == -1:
            nearest_tower_id = find_neareat_enemy_tower_in_kill_model(current_hero["position"], towers, mycamp)
            if nearest_tower_id != -1:
                return cmd_attack(current_hero["id"], "tower", nearest_tower_id)
            else:
                return None
        else:
            h = find_hero_by_id(nearest_enemy_id, heros)
            nearest_tower_id = find_neareat_enemy_tower_in_kill_model(current_hero["position"], towers, mycamp)
            distance_enemy = get_distance(current_hero["position"], h["position"])

            if nearest_tower_id == -1:
                return cmd_attack(current_hero["id"], "hero", nearest_enemy_id)
            else:
                if distance_enemy <= current_hero["fireRange"]:
                    if current_hero["fireCD"] == 0:
                        return cmd_fire(current_hero["id"], nearest_enemy_id)
                    else:
                        return cmd_attack(current_hero["id"], "hero", nearest_enemy_id)
                else:
                    return cmd_attack(current_hero["id"], "tower", nearest_tower_id)

    elif current_hero["status"] in ["waitingFire"]:
        return cmd_attack(current_hero["id"], "hero", executingCmd["targetId"])
    elif current_hero["status"] in ["attacking", "waitingAttack"]:
        if executingCmd["type"] == "tower":
            if current_hero["name"] == "shooter":
                nearest_enemy_id = find_nearest_enemy_hero_in_kill_model(current_hero["position"], heros, mycamp, assigned_hero)
                if nearest_enemy_id == -1:
                    return None
                h = find_hero_by_id(nearest_enemy_id, heros)
                nearest_tower_id = find_neareat_enemy_tower_in_kill_model(current_hero["position"], towers, mycamp)
                distance_enemy = get_distance(current_hero["position"], h["position"])

                if distance_enemy <= current_hero["fireRange"]:
                    return cmd_attack(current_hero["id"], "hero", nearest_enemy_id)
                else:
                    return cmd_attack(current_hero["id"], "tower", nearest_tower_id)

            else:
                return None
        elif current_hero["fireCD"] == 0:
            return cmd_fire(current_hero["id"], executingCmd["targetId"])
        else:
            return None
    elif current_hero["status"] == "moving":
        nearest_enemy_id = find_nearest_enemy_hero_in_kill_model(current_hero["position"], heros, mycamp, assigned_hero)
        if nearest_enemy_id == -1:
            return None
        h = find_hero_by_id(nearest_enemy_id, heros)
        nearest_tower_id = find_neareat_enemy_tower_in_kill_model(current_hero["position"], towers, mycamp)
        distance_enemy = get_distance(current_hero["position"], h["position"])

        if distance_enemy <= current_hero["fireRange"]:
            if current_hero["fireCD"] == 0:
                return cmd_fire(current_hero["id"], nearest_enemy_id)
            else:
                return cmd_attack(current_hero["id"], "hero", nearest_enemy_id)
        else:
            return cmd_attack(current_hero["id"], "tower", nearest_tower_id)

    return None

def find_neareat_enemy_tower_remain_model(hero_positon, towers, mycamp, assigned_tower):
    print "assigned_tower ", assigned_tower
    nearest_tower_id = -1
    min_distance = 1e10
    for tower in towers:
        if tower["camp"] == mycamp:
            continue
        if tower["id"] in assigned_tower:
            continue
        if tower["healthPoint"] > TOWER_LOW_BLOOD:
            continue
        distance = get_distance(tower["position"], hero_positon)
        if distance < min_distance:
            min_distance = distance
            nearest_tower_id = tower["id"]
    if nearest_tower_id != -1:
        assigned_tower.append(nearest_tower_id)
    return nearest_tower_id

def find_neareat_enemy_tower_remain_model_last(hero_positon, towers, mycamp, assigned_tower):
    print "assigned_tower ", assigned_tower
    nearest_tower_id = -1
    min_distance = 1e10
    for tower in towers:
        if tower["camp"] == mycamp:
            continue
        # if tower["id"] in assigned_tower:
        #     continue
        # if tower["healthPoint"] > TOWER_LOW_BLOOD:
        #     continue
        distance = get_distance(tower["position"], hero_positon)
        if distance < min_distance:
            min_distance = distance
            nearest_tower_id = tower["id"]
    # if nearest_tower_id != -1:
    #     assigned_tower.append(nearest_tower_id)
    return nearest_tower_id

def remain_tower_kill(current_hero, heros, towers, mycamp, camps, game_time, assigned_tower):

    nearest_tower_id = find_neareat_enemy_tower_remain_model(current_hero["position"], towers, mycamp, assigned_tower)
    if nearest_tower_id != -1:
        tower = find_tower_by_id(nearest_tower_id, towers)
        return cmd_attack(current_hero["id"], "tower", tower["id"])
    else:
        nearest_tower_id = find_neareat_enemy_tower_remain_model_last(current_hero["position"], towers, mycamp,assigned_tower)
        if nearest_tower_id != -1:
            tower = find_tower_by_id(nearest_tower_id, towers)
            return cmd_attack(current_hero["id"], "tower", tower["id"])
        else:
            nearest_enemy_hero_id = find_nearest_enemy_hero(current_hero["position"], heros, mycamp)
            if nearest_enemy_hero_id != -1:
                return cmd_attack(current_hero["id"], "hero", nearest_enemy_hero_id)
            else:
                return None


def update(message):

    mycamp = message['myCamp']
    states = message['state']
    heros = states['heros']
    towers = states['towers']
    camps = states["camps"]
    game_time = states["time"]
    cmds = []
    assigned_tower = []
    assigned_hero = []

    # for hero in heros:
    #     if hero["camp"] != mycamp:
    #         continue
    #     cmds.append(kill(hero, heros, towers, mycamp))

    # if game_time < DEARTH_TIME:
    #     for hero in heros:
    #         if hero["camp"] != mycamp:
    #             continue
    #         cc = kill(hero, heros, towers, mycamp, assigned_hero)
    #         if not cc is None:
    #             print assigned_hero
    #         cmds.append(cc)
    # else:
    #     # print message
    #     for hero in heros:
    #         if hero["camp"] != mycamp:
    #             continue
    #         statu = check_state(hero)
    #         cc = switch[statu](hero, heros, towers, mycamp, camps, game_time, assigned_tower)
    #         # if not cc is None:
    #         #     print hero
    #         #     print hero["id"], hero["name"], statu, cc
    #         #     print assigned_tower
    #         cmds.append(cc)
    # print message
    if game_time < DEARTH_TIME:
        for hero in heros:
            if hero["camp"] != mycamp:
                continue
            statu = check_state(hero)
            cc = switch[statu](hero, heros, towers, mycamp, camps, game_time, assigned_tower)
            if not cc is None:
                cc
            cmds.append(cc)
    else:
        for hero in heros:
            if hero["camp"] != mycamp:
                continue
            cc = remain_tower_kill(hero, heros, towers, mycamp, camps, game_time, assigned_tower)
            cmds.append(cc)
    return cmds


# http://mobaai.smartstudy.com/?id=15v00
if __name__ == "__main__":
    update("")
