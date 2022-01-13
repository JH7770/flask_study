from app_init import create_app

app = create_app()


@app.route('/ping', methods=['GET'])
def hello_world():  
    return 'pong'


if __name__ == '__main__':
    app.run(debug=True)
