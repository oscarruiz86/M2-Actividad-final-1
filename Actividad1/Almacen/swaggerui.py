from flask_swagger_ui import get_swaggerui_blueprint

def swaggerui():
    SWAGGER_URL = '/api/docs'
    API_URL = '/services/spec'

    # Call factory function to create our blueprint
    return get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        },
    )
