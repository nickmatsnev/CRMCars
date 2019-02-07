

def get_name(_class_):
    name = ""
    try:
        name = object.__class__.__name__
    except:
        name = "Incorrect object"
    finally:
        return name

