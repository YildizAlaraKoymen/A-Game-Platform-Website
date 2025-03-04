import re


from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "123"


def validatePassword(password):
    if not password:
        return "Password must be entered."
    if len(password) < 10:
        return "Password must be at least 10 characters long."
    if not any(c.isdigit() for c in password):
        return "Password must include at least one digit."
    if not any(c.islower() for c in password):
        return "Password must include at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return "Password must include at least one uppercase letter."

# Form Validation
def validateForm():
    username = request.form.get("username", "").strip()
    password = request.form.get("pwd", "").strip()
    fullname = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    # Validation checks
    if not password:
        return "Password must be entered."
    if len(password) < 10:
        return "Password must be at least 10 characters long."
    if not any(c.isdigit() for c in password):
        return "Password must include at least one digit."
    if not any(c.islower() for c in password):
        return "Password must include at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return "Password must include at least one uppercase letter."
    if not username:
        return "Username must be entered."
    if not fullname:
        return "Full name must be entered."
    if not email:
        return "Email address must be entered."


    # Validate email format (basic validation for a valid email address)
    email_format = re.compile(r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$')
    if not email_format.match(email):
        return "Please provide a valid email address."

    return None  # If all validations pass


@app.route("/")
@app.route("/homepage")
@app.route("/homepage", methods=["GET", "POST"])
def homepage():
    conn = sqlite3.connect("game.db")
    c = conn.cursor()

    # Fetch all genres for the dropdown
    c.execute("SELECT DISTINCT name FROM Genre")
    genres = [row[0] for row in c.fetchall()]

    games_by_genre = {}
    keyword = ""
    selected_genre = "All Genres"

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        selected_genre = request.form.get("genre", "All Genres")
        like_keyword = f"%{keyword}%"

        if selected_genre == "All Genres":
            # Search across all genres
            c.execute("""
                SELECT g.title, g.description, gen.name AS genre
                FROM Game g
                LEFT JOIN GenreOfGame gog ON g.gameID = gog.gameID
                LEFT JOIN Genre gen ON gog.genreID = gen.genreID
                WHERE g.title LIKE ? OR g.description LIKE ? OR gen.name LIKE ?
            """, (like_keyword, like_keyword, like_keyword))
            results = c.fetchall()

            # Organize games by genre
            for title, description, genre in results:
                if genre not in games_by_genre:
                    games_by_genre[genre] = []
                games_by_genre[genre].append((title, description))
        else:
            # Search within a specific genre
            c.execute("""
                SELECT g.title, g.description, gen.name AS genre
                FROM Game g
                LEFT JOIN GenreOfGame gog ON g.gameID = gog.gameID
                LEFT JOIN Genre gen ON gog.genreID = gen.genreID
                WHERE (g.title LIKE ? OR g.description LIKE ?) AND gen.name = ?
            """, (like_keyword, like_keyword, selected_genre))
            results = c.fetchall()
            games_by_genre[selected_genre] = [(title, description) for title, description, _ in results]

    conn.close()
    if "username" in session:
        conn = sqlite3.connect("game.db")
        c = conn.cursor()
        username = session["username"]
        c.execute("SELECT isAdmin FROM User WHERE username = ?", (username,))
        val = c.fetchone()
        if val is None:
            return render_template("homepage.html", genres=genres, games_by_genre=games_by_genre,
                               keyword=keyword, selected_genre=selected_genre)
        else:
            isAdmin = val[0]
            return render_template("homepage.html", genres=genres, games_by_genre=games_by_genre,
                               keyword=keyword, selected_genre=selected_genre, username=username, isAdmin=isAdmin)
    else:
        return render_template("homepage.html", genres=genres, games_by_genre=games_by_genre,
                               keyword=keyword, selected_genre=selected_genre)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Validate form data
        validation_error = validateForm()
        if validation_error:
            return render_template("register.html", error=validation_error,
                                   username=request.form.get("username", ""),
                                   fullname=request.form.get("full_name", ""),
                                   email=request.form.get("email", ""))

        #Getting form data
        username = request.form["username"]
        password = request.form["pwd"]
        fullname = request.form["full_name"]
        email = request.form["email"]


        conn = sqlite3.connect("game.db")
        c = conn.cursor()

        # Check if the username already exists
        c.execute("SELECT * FROM User WHERE username = ?", (username,))
        if c.fetchone():
            conn.close()
            return render_template("register.html", error="Username already exists.",
                                   username=username, fullname=fullname, email=email)

        # Determine if the user is an admin based on the email address
        isAdmin = 1 if email.endswith("@game.metu.edu.tr") else 0

        # Insert the new user
        c.execute("INSERT INTO User(username, password, name, email, isAdmin) VALUES (?, ?, ?, ?, ?)",
                  (username, password, fullname, email, isAdmin))


        conn.commit()
        conn.close()

        # Store the username in the session
        session["username"] = username

        # Redirect to the confirmation page
        operation = "0"
        return render_template("confirmation.html", operation = operation)


    return render_template("register.html")


@app.route("/confirmation")
#when the registration is completed successfully the user is directed to confirmation page
def confirmation():
    return render_template("confirmation.html", confirmation = confirmation)

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        pwd = request.form['pwd']

        conn = sqlite3.connect("game.db")
        c = conn.cursor()

        # Fetch the stored password for the given username
        c.execute("SELECT password FROM User WHERE username = ?", (username,))
        user = c.fetchone()

        # If username is not correct
        if not user:
            error = "Username not found."
            return render_template("login.html", error=error)

        # If password is not correct
        if user[0] != pwd:
            error = "Wrong password."
            return render_template("login.html", error=error)

        # Successful login
        session['username'] = username

        # Fetch updated data
        c.execute("SELECT isAdmin FROM User WHERE username = ?", (username,))
        isAdmin = c.fetchone()[0]
        conn.close()
        return redirect(url_for("homepage"))

        # Render login form for GET request
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("homepage"))

def published_games_form():
    title = request.form.get("title", "").strip()
    price = request.form.get("price", "").strip()
    genres = request.form.getlist("genre[]")
    description = request.form.get("description", "").strip()
    isFullRelease = request.form.get("isFullRelease", "").strip()

    if not title:
        return "Title must be entered."
    if not price:
        return "Price must be entered."
    if not genres:
        return "At least one genre must be selected."
    return None # If all validations pass

@app.route("/publishedgames", methods=["GET", "POST"])
def publishedgames():
    if "username" in session:
        conn = sqlite3.connect("game.db")
        c = conn.cursor()

        # Filter games by the currently logged-in user
        username = session["username"]
        c.execute("""
            SELECT g.gameID, g.title, g.price, group_concat(gen.name, ', ') AS genres
            FROM Game g
            LEFT JOIN GenreOfGame gog ON g.gameID = gog.gameID
            LEFT JOIN Genre gen ON gog.genreID = gen.genreID
            WHERE g.username = ?
            GROUP BY g.gameID, g.title, g.price
        """, (username,))
        games_with_genres = c.fetchall()

        if request.method == "POST":
            # Validate form data
            validation_error = published_games_form()
            if validation_error:
                return render_template("publishedgames.html", games=games_with_genres, error=validation_error,
                                       title=request.form.get("title", ""),
                                       price=request.form.get("price", ""),
                                       genres=request.form.getlist("genre[]"),
                                       description=request.form.get("description", ""),
                                       isFullRelease=request.form.get("isFullRelease", ""))

            # Insert the new game
            title = request.form["title"]
            price = request.form["price"]
            genres = request.form.getlist("genre[]")
            description = request.form["description"]
            isFullRelease = request.form["isFullRelease"]

            # Insert into the Game table
            c.execute("INSERT INTO Game(price, title, isFullRelease, description, username) VALUES (?, ?, ?, ?, ?)",
                      (price, title, isFullRelease, description, username))
            game_id = c.lastrowid

            # Insert genres and relationships
            for genre in genres:
                # Check if the genre exists; if not, insert it
                c.execute("SELECT genreID FROM Genre WHERE name = ?", (genre,))
                genre_row = c.fetchone()
                if not genre_row:
                    c.execute("INSERT INTO Genre(name) VALUES (?)", (genre,))
                    genre_id = c.lastrowid
                else:
                    genre_id = genre_row[0]

                # Link the genre to the game
                c.execute("INSERT INTO GenreOfGame(gameID, genreID) VALUES (?, ?)", (game_id, genre_id))

            conn.commit()

            # Refresh the games with genres data for the logged-in user
            c.execute("""
                SELECT g.gameID, g.title, g.price, group_concat(gen.name, ', ') AS genres
                FROM Game g
                LEFT JOIN GenreOfGame gog ON g.gameID = gog.gameID
                LEFT JOIN Genre gen ON gog.genreID = gen.genreID
                WHERE g.username = ?
                GROUP BY g.gameID, g.title, g.price
            """, (username,))
            games_with_genres = c.fetchall()

        conn.close()
        return render_template("publishedgames.html", games=games_with_genres)

    return render_template("homepage.html")

@app.route("/delete_game", methods=["POST"])
def delete_game():
    game_id = request.form.get("game_id")
    if not game_id:
        return redirect(url_for("publishedgames"))

    conn = sqlite3.connect("game.db")
    c = conn.cursor()

    # Delete the game and its associated relationships
    c.execute("DELETE FROM Game WHERE gameID = ?", (game_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("publishedgames"))

@app.route("/myprofile", methods=["GET", "POST"])
def myprofile():
    if "username" in session:
        conn = sqlite3.connect("game.db")
        c = conn.cursor()
        c.execute("SELECT * FROM User WHERE username = ?", (session["username"],))
        user = c.fetchone()
        if request.method == "POST":
            password = request.form.get("pwd", "").strip()
            validation_error = validatePassword(password)
            if validation_error:
                return render_template("myprofile.html", user = user, error = validation_error)

            c.execute("UPDATE User SET password = ? WHERE username = ?", (password, session["username"]))
            conn.commit()
            operation = "1"
            return render_template("confirmation.html", operation=operation)

        # Fetch updated data
        c.execute("SELECT * FROM User WHERE username = ?", (session["username"],))
        user = c.fetchone()
        conn.close()

        return render_template("myprofile.html", user = user)
    else:
        return render_template("homepage.html")

@app.route("/managegenres", methods=["GET", "POST"])
def managegenres():
    # Checking if the user is logged in
    if "username" not in session:
        return redirect(url_for("homepage"))

    # Connect to the database
    conn = sqlite3.connect("game.db")
    c = conn.cursor()

    # Fetching current genres from the database
    c.execute("SELECT * FROM Genre")
    genres = c.fetchall()

    error = None

    if request.method == "POST":
        genre_name = request.form.get("genre_name", "").strip()

        # Validating genre name
        if not genre_name:
            error = "Genre name cannot be empty."
        else:
            # Check if the genre already exists
            c.execute("SELECT * FROM Genre WHERE name = ?", (genre_name,))
            if c.fetchone():
                error = "Genre already exists."
            else:
                # Inserting new genre into the database
                c.execute("INSERT INTO Genre (name) VALUES (?)", (genre_name,))
                conn.commit()
                # Redirecting to refresh the page and show the updated list
                return redirect(url_for("managegenres"))

    conn.close()

    # Rendering the manage genres page
    return render_template("managegenres.html", genres=genres, error=error)

if __name__ == "__main__":
    app.run(debug=True)
