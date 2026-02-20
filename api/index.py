def handler(event, context):
    path = event.get('path', '/')
    
    if path == '/health':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': '{"status": "healthy"}'
        }
    elif path == '/':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': '{"message": "Security Scanner API", "version": "1.0.0", "status": "running"}'
        }
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': '{"error": "Not found"}'
        }