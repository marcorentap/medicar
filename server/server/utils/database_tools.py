def remove_instance_state(item):
    dictionary = item.__dict__
    if('_sa_instance_state' in dictionary):
        del dictionary['_sa_instance_state']
    return dictionary

def list_remove_instance_state(items):
    return [remove_instance_state(item) for item in items]