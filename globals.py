import pickle, logging, os


def to_minutes(hours, minutes):
    return hours*60 + minutes


def to_hours(minutes):
    return [int(minutes/60), minutes%60]


def fix_file_path(path, mkdir=False) :
        if os.name == "nt" :
            path = path.replace("/", "\\")
            #logging.debug(path)
            #logging.debug(os.name)
            logging.debug("Fixed file path: " + path)
        if not os.path.exists(path) and mkdir:
            os.makedirs(path)
            logging.debug("created new directory with path: " + path)
        return path

def store_object(obj, path, name):
    path = fix_file_path(path, True)
    pickle.dump(obj, open(path + name + ".pkl", "wb"), protocol=pickle.HIGHEST_PROTOCOL)


def restore_object(path, name):
    path = fix_file_path(path, False)
    try:
        return pickle.load( open(path + name + ".pkl","rb") )
    except FileNotFoundError :
        #logging.error("Globals: restore_object: Restore File or Folder not found. Your path: \n" + path)
        raise Exception()
