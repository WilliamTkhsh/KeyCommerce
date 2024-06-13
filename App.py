from flask import Flask, jsonify
from Controller.user import user_route
from flask_swagger_ui import get_swaggerui_blueprint
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

app.register_blueprint(user_route, url_prefix="/users")

db.init_app(app)

#@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

#@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message":"Signature verification failed", "error": "invalid_token"}), 401

#@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "Missing token", "error": "authorization_header"}), 401

@app.route('/')
def Index():
    return "Hello from Flask"

if __name__ == "__main__":
    app.run(debug=True)

