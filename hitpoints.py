import random
import csv
from pprint import pprint
from math import ceil, floor



def read_attribs(file):
    csv_dict=dict()
    ind = 1
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_dict[ind] = row
            ind += 1
    return csv_dict



def roll_dice(num_rolls, num_sides):
    # https://docs.python.org/3.6/library/random.html
    # I use the choices routine so it picks k times from the options given in the range from 1 to num_sides
    rolls=random.choices(range(1, num_sides+1), k=num_rolls)
    return sum(rolls)


def lookup_offense():
    print('\n' * 2)

    ''' Get Character 1 choice '''
    print(' Choose Character 1 (Offense)\n', '=' * 28, '\n')
    character_dict = read_attribs('Character_Attributes.csv')
    for key in character_dict.keys():
        print('{}: {}'.format(str(key), character_dict[key]['Name']))
    character1_choice = int(input('\nEnter Character 1 Choice: '))  # Ask for user input
    c1_attribs = character_dict[character1_choice]
    # print("You chose: ", c1_attribs)

    ''' Remap weapons skills to nested dictionary '''
    c1_attribs['Skill'] = dict()
    print('\n' * 2)
    for key in c1_attribs.keys():
        split_key = key.split()
        if len(split_key) > 1 and split_key[-1] == 'Skill':
            c1_attribs['Skill'][' '.join(split_key[:-1])] = c1_attribs[key]



    print('\n' * 2)

    ''' Get weapon choice '''
    print(' Character 1 Weapon\n', '=' * 18, '\n')
    weapons_dict = read_attribs('Weapons_Attributes.csv')
    for key in weapons_dict.keys():
        print('{}: {}'.format(str(key), weapons_dict[key]['Name']))
    weapon_choice = int(input('\nEnter Weapon Choice: '))  # Ask for user input
    weapon_attribs = weapons_dict[weapon_choice]
    # print("You chose: ", weapon_attribs)

    c1_attribs['Weapon'] = weapon_attribs

    c1_attribs['Shooting Skill'] = int(c1_attribs['Dexterity']) + int(c1_attribs['Skill'][weapon_attribs['Class']])

    pprint(c1_attribs)
    return c1_attribs


def lookup_defence():
    print('\n' * 2)

    ''' Get Character 2 choice '''
    print(' Choose Character 2 (Defense)\n', '=' * 28, '\n')
    character_dict = read_attribs('Character_Attributes.csv')
    for key in character_dict.keys():
        print('{}: {}'.format(str(key), character_dict[key]['Name']))
    character2_choice = int(input('\nEnter Character 2 Choice: '))  # Ask for user input
    c2_attribs = character_dict[character2_choice]
    # print("You chose: ", c2_attribs)

    print('\n' * 2)

    ''' Get Character 2 Position Value '''
    c2_attribs['Position Value'] = input('\nEnter Character 2 Position Value: ')
    # print("You chose: ", c2_attribs)

    pprint(c2_attribs)
    return c2_attribs


def shots_fired_calc(offense, defence):

    print('Shooting Skill: ', int(offense['Shooting Skill']))
    fire_rate = int(offense['Weapon']['Fire Rate'])
    print('Fire rate: ', fire_rate)
    fire_rate_array = [4] * int(floor(fire_rate / 4.0))
    if fire_rate % 4 > 0:
        fire_rate_array.append(fire_rate % 4)
    print('fire_rate_array: ',fire_rate_array)


    skills_gap_array = [int(offense['Shooting Skill'])] * len(fire_rate_array)
    for ind in range(len(fire_rate_array)):
        skills_gap_array[ind] -= roll_dice(3, 6) + int(defence['Position Value'])
    print('skills_gap_array calced: ', skills_gap_array)

    for ind in range(len(skills_gap_array)):
        if skills_gap_array[ind] < 0:
            skills_gap_array[ind] = 0
        elif skills_gap_array[ind] == 0:
            skills_gap_array[ind] = 1
        elif skills_gap_array[ind] > fire_rate_array[ind]:
            skills_gap_array[ind] = fire_rate_array[ind]
    print('skills_gap_array returned: ', skills_gap_array)

    return sum(skills_gap_array)

def fired_hits_calc(offense, defence, shots_fired):
    print('\n' * 2)

    dodge = flor((int(defence['Dexterity']) + int(defence['Health'])) / 4.0)
    print('dodge: ', dodge)
    fired_hits = roll_dice(3, 6) - dodge - int(defence['Armor'])
    print('actual fired-hits: ', fired_hits)
    if fired_hits > shots_fired:
        fired_hits = shots_fired
    elif fired_hits < 0:
        fired_hits = 0
    return fired_hits


def damage_pts_calc(offense, defence, fired_hits):
    print('\n' * 2)

    if offense['Weapon']['Class'] == 'Sword':
        damage_rolls = int(offense['Strength'])
    else:
        damage_rolls = int(offense['Weapon']['Damage Rolls'])
    damage_pts = fired_hits * (roll_dice(damage_rolls, 6) + int(offense['Weapon']['Damage Constant']))
    return damage_pts


def main():

    offense = lookup_offense()

    defence = lookup_defence()

    shots_fired = shots_fired_calc(offense, defence)
    print('returned shots_fired: ', shots_fired)
    # shots_fired = 20

    fired_hits = fired_hits_calc(offense, defence, shots_fired)
    print('returned fired_hits: ', fired_hits)

    damage_pts = damage_pts_calc(offense, defence, fired_hits)

    print('{} hit {} with {} {} times, resulting in {} damage.'.format(
        offense['Name'],
        defence['Name'],
        offense['Weapon']['Name'],
        fired_hits,
        damage_pts))


if __name__ == '__main__':
    main()
