from myflask import MyFlask as ApiFlask
import user

app = ApiFlask(__name__, static_folder=None)

app.register_blueprint(user.user, url_prefix='/api/auth/user')

if __name__ == "__main__":
    print('Spinning up server')
    print(app.url_map)
    app.run(host='0.0.0.0', port='80')