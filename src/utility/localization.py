from configparser import RawConfigParser

# TODO: Cache this.

def localize(mod, key):
    try:
        p = RawConfigParser()
        p.read("/home/dp/Programming/Eowyne/static/txt/" + mod + ".ini")
        [section, option] = key.split(".", 1)
        return p.get(section, option)
    except Exception as e:
        print(e)
        return "YOLO"