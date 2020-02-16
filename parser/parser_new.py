from transliterate import translit


def email(s, n):
    ret = translit(s.lower(), 'ru', reversed=True) + "." + translit(n.lower(), 'ru', reversed=True) + "@company.com"
    ret = ret.replace('\'', '')
    return ret


def get_place_id(room, plc):
    x = (room, plc)
    res = False
    if x not in dict_id:
        dict_id[x] = len(dict_id) + 1
        res = True
    return dict_id[x], res


dict_id = dict()
fin = '../data/users.txt'

floor = -1
room_id = 0
user_id = 0

offices = dict()
with open('config.ini', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        fall, s = line.split(' : ')
        ss, sf = map(int, s.split('-'))
        for f in fall.split(','):
            f = f.strip()
            if '-' in f:
                start, finish = f.split('-')
            else:
                start, finish = f, f
            while True:
                offices[start] = list(range(ss, sf + 1))
                if start == finish:
                    break
                start = str(int(start) + 1) if start[-1] != 'А' else str(int(start[:-1]) + 1) + 'А'

of2id = dict()

with open('users.csv', 'w', encoding='utf-8') as users_file:
    with open('places.csv', 'w', encoding='utf-8') as places_file:
        with open('rooms.csv', 'w', encoding='utf-8') as rooms_file:

            print("id;floor;name;type;x;y", file=rooms_file)
            print("id;email;password;surname;name;place_id", file=users_file)
            print("id;number;room_id", file=places_file)

            with open(fin, 'r', encoding='utf-8') as inp:
                for line in inp:
                    line = line.strip()
                    if line.startswith('Те же') or len(line) == 0:
                        continue

                    if line.endswith('этаж'):
                        floor = line.split()[0]
                    elif '–' in line:
                        rng, name = line.split(' – ')
                        if '-' in rng:
                            start, finish = rng.split('-')
                        else:
                            start, finish = rng, rng
                        if int(start.strip('А')) > int(finish.strip('А')):
                            start, finish = finish, start
                        while True:
                            if start not in offices:
                                offices[start] = [-1]
                            room_id += 1
                            of2id[start] = room_id
                            print(room_id, floor, start, name, 0, 0, sep=';', file=rooms_file)
                            if start == finish:
                                break
                            start = str(int(start) + 1) if start[-1] != 'А' \
                                else str(int(start[:-1]) + 1) + 'А'
                    else:
                        if ' ' not in line:
                            print(line)
                            line += ' '
                        sur, name = line.split(' ')
                        user_id += 1
                        if len(offices[start]) == 0:
                            place = 1
                        else:
                            place = offices[start][0]
                            if place != -1:
                                offices[start].pop(0)
                        place_id, f = get_place_id(start, place)
                        print(user_id, email(sur, name), "12345", sur, name, place_id, sep=';', file=users_file)
                        if f:
                            print(place_id, place, room_id, sep=';', file=places_file)
            for key, value in offices.items():
                for place in value:
                    place_id, f = get_place_id(key, place)
                    if f:
                        print(place_id, place, of2id[key], sep=';', file=places_file)