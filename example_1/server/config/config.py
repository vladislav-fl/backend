class Constants:
    class URL:
        PROTOCOL: str = 'http'
        IP: str = '127.0.0.1'
        PORT: str = '8000'

        ADDRESS: str = f'{PROTOCOL}://{IP}:{PORT}/'
    
    class API:
        GET: dict = {
            '/': {
                'INFO':       'RETURN MAIN ADDRESS',
                'ARGUMENTS':   None,
                'RETURN':     'JSON',

                'AVAILABLE': True,
            }
        }

        POST: dict = {
            '/': {
                'INFO':       'RETURN MAIN ADDRESS',
                'ARGUMENTS':   None,
                'RETURN':     'JSON',

                'AVAILABLE': True,
            }
        }

        PUT: dict = {
            '/': {
                'INFO':       'RETURN MAIN ADDRESS',
                'ARGUMENTS':   None,
                'RETURN':     'JSON',

                'AVAILABLE': True,
            }
        }

        DELETE: dict = {
            '/': {
                'INFO':       'RETURN MAIN ADDRESS',
                'ARGUMENTS':   None,
                'RETURN':     'JSON',

                'AVAILABLE': True,
            }
        }