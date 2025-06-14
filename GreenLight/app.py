from config import Config
from greenlight import create_app

app = create_app(Config)


if __name__ == '__main__':
    app.run(debug=True)



