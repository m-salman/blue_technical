import json

def build_response(status, reason):
    return json.dumps({'status': status, 'reason': reason})
