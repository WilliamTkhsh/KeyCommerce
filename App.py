from flask import Flask
from Controller.user import user_route
from Controller.keycaps import keycaps_route
from Controller.switches import switch_route
from Controller.boards import board_route
from Controller.keyboard import keyboard_route
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from database import db

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://keycommerce.swagger.io/v2/swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)
app.register_blueprint(swaggerui_blueprint)

load_dotenv()

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{db_user}:{db_password}@localhost:3306/{db_name}".format(db_user=db_user, db_password=db_password, db_name=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET']

jwt = JWTManager(app)
@jwt.additional_claims_loader
def make_additional_claims(identity):
    if identity == os.environ['ADMIN_ID']:
        return {"is_staff": True}
    return {"is_staff": False}

app.register_blueprint(user_route, url_prefix="/users")
app.register_blueprint(switch_route, url_prefix="/switches")
app.register_blueprint(keycaps_route, url_prefix="/keycaps")
app.register_blueprint(board_route, url_prefix="/boards")
app.register_blueprint(keyboard_route, url_prefix="/keyboard")
db.init_app(app)

@app.route('/')
def Index():
    return "Hello from Flask"

if __name__ == "__main__":
    app.run(debug=True)

