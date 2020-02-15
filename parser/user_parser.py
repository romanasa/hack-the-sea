# coding=utf-8
input = "../data/users.txt"
users = open("users.csv", "w", encoding='utf-8')
rooms = open("rooms.csv", "w", encoding='utf-8')
places = open("places.csv", "w", encoding='utf-8')

from transliterate import translit


def email(s, n):
    ret = translit(s.lower(), 'ru', reversed=True) + "." + translit(n.lower(), 'ru', reversed=True) + "@company.com"
    ret = ret.replace('\'', '')
    return ret

id_users = 0
id_places = 0
id_rooms = 0
lines = []

for line in open(input, "r", encoding="utf-8"):
    if (len(line) == 0): continue
    lines.append(line)

print("id;floor;name;type;x;y", file=rooms)
print("id;email;password;surname;name", file=users)
print("id;number;user_id;room_id", file=places)

floor = -1
place = ""
type = ""
cabinet = 0

pl = {} # [place_id][room_id] = us


for j in range(len(lines)):
    line = lines[j]
    v = line.split()
    if (len(v) == 0): continue
    if (v[0] == "Те"): continue
    if (v[0].isdigit() or (v[0][-1] == "А" and v[0][:-1].isdigit()) or ('-' in v[0])):
        if (v[1] == "этаж"):
            floor = v[0].strip()
            cabinet = 0
            if (floor[-1] == 'А'):
                cabinet = 12
        if (v[1] == "–"):
            place, type = line.split("–")
            place = place.strip()
            type = type.strip()
            cabinet = 0
            if (place[-1] == 'А'):
                cabinet = 12
            if ("-" in place):
                fr, to = map(int, place.split("-"))
                for i in range(fr, to + 1):
                    id_rooms += 1
                    print(id_rooms, floor, i, type, 0, 0, sep=';', file=rooms)
            else:
                id_rooms += 1
                print(id_rooms, floor, place, type, 0, 0, sep=';', file=rooms)
    else:
        if ('-' in v[0]): continue
        id_users += 1
        if (len(v) == 1): v.append(v[0])
        print(id_users, email(v[0], v[1]), "12345", v[0], v[1], sep=';', file=users)
        id_places += 1
        cabinet += 1
        print(id_places, cabinet, id_users, id_rooms, sep=';', file=places)

places.close()
users.close()
rooms.close()












