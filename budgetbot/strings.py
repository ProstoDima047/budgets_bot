import json
from string import Template

def load_locale(locale): # locale as in "ua", "en", etc
    f = open('locale_' + locale + '.json')
    return json.load(f)
    
locale = 'ua'

def get_string(key, **kwargs):
    try: 
        data = load_locale(locale)
        return Template(data[key]).safe_substitute(**kwargs)
    except:
        return key