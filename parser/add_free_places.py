offices = dict()
with open('config.ini', 'r') as file:
    for line in file.readlines()[1:]:
        f, s = line.split(' : ')
        s = int(s)
        if '-' in f:
            start, finish = f.split('-')
        else:
            start, finish = f, f
        while start != finish:
            st_num = s + 1 if start[-1] == 'A' else 1
            offices[start] = list(range(st_num, st_num + int(s)))
            start = str(int(start) + 1) if start[-1] != 'A' else str(int(start[:-1]) + 1) + 'A'

id2room = [-1]
with open('rooms.csv', 'r', encoding='utf-8') as file:
    for line in file.readlines()[1:]:
        s = line.split(';')[2]
        id2room += [s]
        if s not in offices:
            offices[s] = [1]

with open('places.csv', 'r') as file:
    for line in file.readlines()[1:]:
        spl = list(map(int, line.split(';')))
        offices[id2room[spl[2]]].remove(spl[1])

with open('places.csv', 'a', encoding='utf-8') as file:
    place_id = spl[0]
    for i, x in enumerate(id2room):
        if x in offices:
            for place in offices[x]:
                place_id += 1
                print(place_id, place, i + 1, sep=';', file=file)
