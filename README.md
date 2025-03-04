# A-Game-Platform-Website
A Game Platform Website that employs Python Flask for server-side scripting with a SQLite database.

Project Overview
This project is a Game Platform Website that allows users to register, publish, and manage video games they have developed. Admin users have additional privileges to manage game genres. The website is built using Python Flask, SQLite, HTML, CSS, and JavaScript.

Technologies Used
Python 3.11
Flask (for server-side scripting)
SQLite (for database management)
HTML & CSS (for front-end structure and design)
JavaScript (for client-side validation and interactivity)

Operating System Used
Windows 11

Project Functionalities
User Functionalities
Registration: Users can register with a username, password, full name, and email.
Login & Logout: Users can log in with valid credentials and log out when needed.
Publish Games: Registered users can add games with details like title, price, and genres.
Manage Games: Users can view, delete, and manage their published games.
Profile Management: Users can view and update their profile details.
Search Games: Games can be searched based on keywords and filtered by genre.

Admin Functionalities
Admin Identification: Users with emails ending in @game.metu.edu.tr are assigned admin roles.
Manage Genres: Admins can create and manage game genres.

Database Schema
Users Table: Stores user information with roles.
Games Table: Stores game details with genre references.
Genres Table: Stores different game genres.

Installation & Setup

Install dependencies:
pip install flask sqlite3

Run the database creation script:
python dbscript.py

Start the Flask application:
python main.py

Open the application in your browser


