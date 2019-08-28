import pickle, logging, inspect, os


def to_minutes(hours, minutes):
    return hours*60 + minutes


def to_hours(minutes):
    return [int(minutes/60), minutes%60]


def fix_file_path(path, mkdir=False) :
        if os.name == "nt" :
            path = path.replace("/", "\\")
            #debug(path)
            #debug(os.name)
            debug("Fixed file path: " + path)
        if mkdir:
            os.makedirs(os.path.dirname(path),exist_ok=True)

            debug("created new directory with path: " + os.path.dirname(path))
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


# from https://stackoverflow.com/a/5500099
logger=logging.getLogger(__name__)
def debug(msg):
    frame,filename,line_number,function_name,lines,index=inspect.getouterframes(
        inspect.currentframe())[1]
    line=lines[0]
    indentation_level=line.find(line.lstrip())
    logger.debug('{i} {m}'.format(
        i='.'*indentation_level,
        m=msg
        ))
