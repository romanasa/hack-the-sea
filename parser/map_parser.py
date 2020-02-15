input = "../data/floor3_map.txt"
out = open("floor3_html.txt", "w")

for line in open(input, "r"):
    v = line.split()
    if (len(v) == 0): continue
    if (not v[0].startswith("<area")): continue
    title = v[3].split('\"')[1]
    href = title
    coords = v[5].split('\"')[1].split(',')
   # print(v)
    for i in range(4): coords[i] = float(coords[i])
    if (coords[2] < coords[0]):
        coords[2], coords[0] = coords[0], coords[2]
        coords[3], coords[1] = coords[1], coords[3]

    coords[2] = (abs(coords[2] - coords[0])) / 1000 * 100
    coords[3] = (abs(coords[3] - coords[1])) / 2040 * 100
    coords[0] = coords[0] / 1000 * 100
    coords[1] = coords[1] / 2040 * 100

    #print("<area target=\"\" alt=\"", title, " title=\"", title, " href=\"", href, " coords=\"", ",".join(coords), " shape=\"poly\">")
    print("<a href=\"", href, "\" style=\"top: ", coords[1], "%; left: ", coords[0], "%; width: ", coords[2], "%; height: ", coords[3], "%;\"></a>", file=out, sep='')