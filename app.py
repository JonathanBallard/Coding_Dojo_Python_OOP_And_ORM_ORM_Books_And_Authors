


from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy			# instead of mysqlconnection
from sqlalchemy.sql import func                         # ADDED THIS LINE FOR DEFAULT TIMESTAMP
from flask_migrate import Migrate			# this is new
app = Flask(__name__)
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///$books_and_authors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)




#### ADDING THIS CLASS ####
# the db.Model in parentheses tells SQLAlchemy that this class represents a table in our database

written_by_table = db.Table('written_by',
db.Column('author_id', db.Integer, db.ForeignKey('Authors.id', ondelete='cascade'), primary_key=True),
db.Column('book_id', db.Integer, db.ForeignKey('Books.id', ondelete='cascade'), primary_key=True))


class Authors(db.Model):	
    __tablename__ = "Authors"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    notes = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    books_written = db.relationship('Books', secondary=written_by_table)



class Books(db.Model):	
    __tablename__ = "Books"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    book_written_by = db.relationship('Authors', secondary=written_by_table)












# routes go here...

@app.route('/')
def index():

    bookList = Books.query.all()


    return render_template('index.html', bookList = bookList)

@app.route('/add_book', methods=["POST"])
def add_book():
    title = request.form['title']
    description = request.form['description']

    new_book = Books(title=title, description = description)
    db.session.add(new_book)
    db.session.commit()
    return redirect('/')


@app.route('/books/<id>')
def book(id):
    authorList = Authors.query.all()
    book = Books.query.get(id)
    return render_template('book.html', book = book, authorList = authorList)




@app.route('/authors/<id>')
def author(id):
    
    author = Authors.query.get(id)
    # bookList = Books.query.all()
    bookList = Books.query.all()
    print('TESTTESTTEST', author.books_written)
    writtenList = author.books_written
    
    return render_template('author.html', author = author, bookList = bookList, written_by = writtenList)



@app.route('/authors')
def authors():

    authorList = Authors.query.all()
    bookList = Books.query.all()
    return render_template('authors.html', authorList = authorList, bookList = bookList)


@app.route('/add_author', methods=["POST"])
def add_author():
    fname = request.form['fname']
    lname = request.form['lname']
    notes = request.form['notes']

    new_author = Authors(first_name=fname, last_name=lname, notes = notes)
    db.session.add(new_author)
    db.session.commit()

    bookList = Books.query.all()
    return redirect('/authors', bookList = bookList)


@app.route('/add_book_relationship', methods=["POST"])
def add_book_relationship():
    
    authorID = request.form['authorID']
    bookID = request.form['book']

    existing_book = Books.query.get(bookID)
    existing_user = Authors.query.get(authorID)
    existing_book.book_written_by.append(existing_user)
    db.session.commit()

    bookList = Books.query.all()
    return redirect('/')


@app.route('/add_author_relationship', methods=["POST"])
def add_author_relationship():
    
    authorID = request.form['author']
    bookID = request.form['bookID']

    existing_book = Books.query.get(bookID)
    existing_user = Authors.query.get(authorID)
    existing_user.books_written.append(existing_book)
    db.session.commit()

    bookList = Books.query.all()
    return redirect('/authors')






if __name__ == "__main__":
    app.run(debug=True)




















