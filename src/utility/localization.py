from configparser import RawConfigParser

# TODO: Cache this.

def localize(mod, key):
    global text_path
    try:
        p = RawConfigParser()
        p.read(text_path + mod + ".ini")
        [section, option] = key.split(".", 1)
        return p.get(section, option)
    except Exception as e:
        print(e)
        return "YOLO"