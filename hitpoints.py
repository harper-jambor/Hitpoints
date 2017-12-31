import random
import csv





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




def main():

    ''' Roll the dice '''
    # dice = roll_dice(3, 6)
    # print("Rolled: {}".format(dice))

    print('\n' * 2)

    ''' Get Character 1 choice '''
    print(' Choose Character 1 (Offense)\n', '=' * 28, '\n')
    character_dict = read_attribs('Character_Attributes.csv')
    for key in character_dict.keys():
        print('{}: {}'.format(str(key), character_dict[key]['Name']))
    character1_choice = int(input('\nCharacter 1 Choice: '))  #Ask for user input
    c1_attribs = character_dict[character1_choice]
    print("You chose: ", c1_attribs)



    print('\n' * 2)

    ''' Get weapon choice '''
    print(' Character 1 Weapon\n', '=' * 18, '\n')
    weapons_dict = read_attribs('Weapons_Attributes.csv')
    for key in weapons_dict.keys():
        print('{}: {}'.format(str(key), weapons_dict[key]['Name']))
    weapon_choice = int(input('\nWeapon Choice: ')) #Ask for user input
    weapon_attribs = weapons_dict[weapon_choice]
    print("You chose: ", weapon_attribs)



    print('\n' * 2)

    ''' Get Character 2 choice '''
    print(' Choose Character 2 (Defense)\n', '=' * 28, '\n')
    for key in character_dict.keys():
        print('{}: {}'.format(str(key), character_dict[key]['Name']))
    character2_choice = int(input('\nCharacter 2 Choice: '))  # Ask for user input
    c2_attribs = character_dict[character2_choice]
    print("You chose: ", c2_attribs)


    print('\n' * 2)

    ''' Get Character 2 Position Value '''
    # print(' Character 2 Position Value\n', '=' * 28, '\n')
    c2_posnval = int(input('\nCharacter 2 Position Value: '))  # Ask for user input
    print("You chose: ", c2_posnval)


if __name__ == '__main__':
    main()