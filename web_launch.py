from flaskr import create_app, users_db, toDoList_db
from datetime import timedelta

__author__ = "Itai Dotan"

session_lif_time = timedelta(hours=1)

if __name__ == "__main__":
    users_db.create_all(app=create_app())
    toDoList_db.create_all(app=create_app())
    app = create_app()
    app.permanent_session_lifetime = session_lif_time
    app.run(debug=True)
