import json

def json_encode(x):
    return json.dumps(x, indent = 2)

def json_decode(x):
    try:
        return json.loads(x)
    except:
        return json.loads(fix_lazy_json(x))

def json_print(x):
    print(json_encode(x))

def find_top_level_json(text):
    nesting = 0
    start_index = None
    ctx = None
    objects = []
    for i, x in enumerate(text):
        if ctx == 'string':
            if x == '"':
                ctx = None
                continue
            continue
        if x == '{':
            if nesting == 0:
                start_index = i
            nesting += 1
            continue
        if x == '}':
            if nesting == 0:
                raise Exception('Invalid JSON')
            nesting -= 1
            if nesting == 0:
                obj_text = text[start_index:i + 1]
                obj = json_decode(obj_text)
                objects.append(obj)
            continue
    return objects

def fix_lazy_json(text):
    import tokenize
    import token
    from io import StringIO
    tokengen = tokenize.generate_tokens(StringIO(text).readline)
    result = []
    for tokid, tokval, _, _, _ in tokengen:
        # fix unquoted strings
        if (tokid == token.NAME):
            if tokval not in ['true', 'false', 'null', '-Infinity', 'Infinity', 'NaN']:
                tokid = token.STRING
                tokval = u'"%s"' % tokval
        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith ("'"):
                tokval = u'"%s"' % tokval[1:-1].replace ('"', '\\"')
        # remove invalid commas
        elif (tokid == token.OP) and ((tokval == '}') or (tokval == ']')):
            if (len(result) > 0) and (result[-1][1] == ','):
                result.pop()
        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith ("'"):
                tokval = u'"%s"' % tokval[1:-1].replace('"', '\\"')
        result.append((tokid, tokval))
    return tokenize.untokenize(result)

def remove_bracketed_hashes(obj):
    import re
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            key = re.sub(r'\(\d+\)$', '', key)
            if key == 'class':
                result[key] = re.sub(r'\(\d+\)$', '', value)
                continue
            result[key] = remove_bracketed_hashes(value)
        return result
    if isinstance(obj, list):
        return [remove_bracketed_hashes(x) for x in obj]
    return obj

def uuid_from_text(text):
    import hashlib
    import uuid
    hasher = hashlib.md5()
    hasher.update(text.encode('utf-8'))
    digest = hasher.digest()
    return str(uuid.UUID(bytes = digest[:16]))

def parse_bitwig_device(device_data):
    ## Extract top level JSON objects
    objects = util.find_top_level_json(device_data)
    if len(objects) != 2:
        raise Exception('Invalid or non-plaintext Bitwig device')

    ## Construct an object
    device = {
        'header': device_data[:40],
        'meta': objects[0],
        'contents': objects[1],
    }

    ## Remove all hashes from keys
    device['meta'] = util.remove_bracketed_hashes(device['meta'])
    device['contents'] = util.remove_bracketed_hashes(device['contents'])
    return device

def serialize_bitwig_device(device):
    return (device['header'] + '\n\n'
        + util.json_encode(device['meta']) + '\n\n'
        + util.json_encode(device['contents']) + '\n')
