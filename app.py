from src import create_app

app = create_app()

if __name__ == "__main__":
    # db.create_all()
    app.run(threaded=True, debug=True)

