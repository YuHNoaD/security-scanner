def handler(request):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": '{"message": "Security Scanner API", "version": "1.0.0", "status": "running"}'
    }

__all__ = ["handler"]