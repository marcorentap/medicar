import json
from lib2to3.pytree import convert

def convert_to_dict(item):
    dictionary = {}
    if(isinstance(item, dict)):
        dictionary = item
    else:
        dictionary = item.__dict__
    return remove_instance_state(dictionary)

def list_convert_to_dict(items):
    return [convert_to_dict(item) for item in items]

def remove_instance_state(dictionary):
    if('_sa_instance_state' in dictionary):
        del dictionary['_sa_instance_state']
    return dictionary

def list_remove_instance_state(items):
    return [remove_instance_state(item) for item in items]

def session_dict_get_kst(session_dict, time):
    if(session_dict[time] is not None):
        return session_dict[time].strftime("%Y-%m-%d %H:%M:%S KST")
    return ""

def session_pre_jsonify(session):
    session_dict = convert_to_dict(session)
    session_dict['measurement_data'] = json.loads(session_dict['measurement_data'])
    session_dict['diagnosis_data'] = json.loads(session_dict['diagnosis_data'])
    session_dict['measurement_time'] = session_dict_get_kst(session_dict, 'measurement_time')
    session_dict['diagnosis_time'] = session_dict_get_kst(session_dict, 'diagnosis_time')
    session_dict['time'] = session_dict_get_kst(session_dict, 'time')
    return session_dict

def sessions_pre_jsonify(sessions):
    return [session_pre_jsonify(session) for session in sessions]