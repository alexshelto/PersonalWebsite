from flaskblog import create_app

app = create_app() #running function to create an instance of the flask app

if __name__ == '__main__':
    app.run(debug=True)
