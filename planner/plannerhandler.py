import globals
from planner.planner import Planner

# relative from rasa/actions/
#__base_path = "../storage/schedules/"

def restore(path, user_id):
    planner = globals.restore_object(
        path,
        str(user_id)
    )
    if not planner:
        planner = Planner()
        globals.store(path, user_id, planner)
    return planner


def store(path, user_id, planner):
    globals.store_object(
        planner,
        path,
        str(user_id)
    )


if __name__ == "__main__":
    planner = restore(1234)
    print(planner)

    #planner.import_ics("./test_snippets/export2.ics")

    store(1234, planner)
