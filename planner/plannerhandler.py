import globals
from planner.planner import Planner

# relative from rasa/actions/
__base_path = "../storage/schedules/"

def restore(user_id):
    try:
        planner = globals.restore_object(
            __base_path,
            str(user_id)
        )
    except Exception:
        planner = Planner()
        store(user_id, planner)
    return planner


def store(user_id, planner):
    globals.store_object(
        planner,
        __base_path,
        str(user_id)
    )


if __name__ == "__main__":
    planner = restore(1234)
    print(planner)

    #planner.import_ics("./test_snippets/export2.ics")

    store(1234, planner)
