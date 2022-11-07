# import create_app function from our app package
from core import create_app

if __name__ == "__main__":
    app = create_app()
    # debug=True will make the server reload itself on code changes
    app.run(debug=True)
