from website import create_app

app = create_app()

# the website is launched in debug mode (updated after changes)
if __name__ == '__main__':
    # запуск приложения и обьявления хоста и порта
    app.run(host="127.0.0.1", port=8900, debug=True)