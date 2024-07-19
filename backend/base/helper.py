def success_response(data, message = 'success'):
    return {
        'status': 200,
        'data': data,
        'message': message
    }

def error_response(message):
    return {
        'status': 400,
        'data': message
    }