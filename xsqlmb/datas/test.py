with open("./a/access.log", "r", encoding="utf-8") as f:
    lines = f.readlines()
    f.close()

with open("c.txt", "w", encoding="utf-8") as f1:
    for x in lines:
        f1.write("Apr 23 07:39:48 192.168.2.161 " + x)
    f1.close()
