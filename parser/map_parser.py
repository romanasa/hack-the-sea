input = "../data/antresol_map.txt"
out = open("antresol_html.txt", "w")

for line in open(input, "r"):
    v = line.split()
    if (len(v) == 0): continue
    if (not v[0].startswith("<area")): continue
    title = v[3].split('\"')[1]
    href = "room/" + title
    coords = v[5].split('\"')[1].split(',')
   # print(v)
    for i in range(4): coords[i] = float(coords[i])
    if (coords[2] < coords[0]):
        coords[2], coords[0] = coords[0], coords[2]
        coords[3], coords[1] = coords[1], coords[3]

    # 600x800 - room
    # 1000x2040 - floor
    coords[2] = (abs(coords[2] - coords[0])) / 600 * 100
    coords[3] = (abs(coords[3] - coords[1])) / 800 * 100
    coords[0] = coords[0] / 600 * 100
    coords[1] = coords[1] / 800 * 100

    #only for rooms
    for i in range(1):
        if (coords[i] < 50):
            coords[i] = 50 - (50 - coords[i]) * 0.6
        else:
            coords[i] = 50 + (coords[i] - 50) * 0.6

    #print("<area target=\"\" alt=\"", title, " title=\"", title, " href=\"", href, " coords=\"", ",".join(coords), " shape=\"poly\">")

    # * 0.6 only for rooms
    print("<a href=\"", href, "\" style=\"top: ", coords[1], "%; left: ", coords[0], "%; width: ", coords[2] * 0.6, "%; height: ", coords[3], "%;\"></a>", file=out, sep='')