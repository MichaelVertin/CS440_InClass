from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)


def get_db_connection():
   conn = sqlite3.connect('books.db')
   conn.row_factory = sqlite3.Row
   return conn


def init_db():
   connection = get_db_connection()
   with open('books.sql', 'r') as f:
       connection.executescript(f.read())
   connection.commit()
   connection.close()


@app.route('/api/books', methods=['GET'])
def get_books():
   conn = get_db_connection()
   books = conn.execute('SELECT * FROM books').fetchall()
   conn.close()
   return jsonify([dict(book) for book in books])


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
   conn = get_db_connection()
   book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
   conn.close()
   if book is None:
       return jsonify({'error': 'Book not found'}), 404
   return jsonify(dict(book))


@app.route('/api/books', methods=['POST'])
def add_book():
   if not request.json:
       return jsonify({'error': 'No data provided'}), 400
  
   required_fields = ['title', 'author', 'year']
   if not all(field in request.json for field in required_fields):
       return jsonify({'error': 'Missing required fields'}), 400
  
   conn = get_db_connection()
   cursor = conn.execute(
       'INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
       (request.json['title'], request.json['author'], request.json['year'])
   )
   book_id = cursor.lastrowid
   conn.commit()
   conn.close()
  
   return jsonify({'id': book_id, 'message': 'Book added successfully'}), 201




@app.route('/api/books/<int:book_id>', methods=['PUT'])
def put_book():
   if not request.json:
       return jsonify({'error': 'No data provided'}), 400
  
   required_fields = ['title', 'author', 'year']
   if not all(field in request.json for field in required_fields):
       return jsonify({'error': 'Missing required fields'}), 400
  
   conn = get_db_connection()
   cursor = conn.execute(
       'INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
       (request.json['title'], request.json['author'], request.json['year'])
   )
   book_id = cursor.lastrowid
   conn.commit()
   conn.close()
  
   return jsonify({'id': book_id, 'message': 'Book added successfully'}), 201


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book():
   conn = get_db_connection()
   cursor = conn.execute(
       'DELETE FROM books WHERE id = ?', (book_id,)
   )
   conn.commit()
   conn.close()
   # assume book exists if book_id can be provided -> return None
   return jsonify(), 201


if __name__ == '__main__':
   init_db()
   app.run(host='0.0.0.0', port=5001)
















@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/books', methods=['GET'])
def books():
    connection = get_db_connection()
    books = connection.execute('SELECT * FROM books').fetchall()
    connection.close()
    return render_template('books.html', books=books)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def book_details(book_id):
    connection = get_db_connection()
    book = connection.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    reviews = connection.execute('SELECT * FROM reviews WHERE book_id = ?', (book_id,)).fetchall()
    connection.close()
    return render_template('reviews.html', book=book, reviews=reviews)

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    
    connection = get_db_connection()
    connection.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
                (title, author, year))
    connection.commit()
    connection.close()
    flash('Book added successfully!')
    return redirect(url_for('books'))

@app.route('/api/books', methods=['POST'])
def api_books():
    connection = get_db_connection()
    books = connection.execute('SELECT * FROM books').fetchall()
    connection.close()
    return jsonify([dict(book) for book in books])

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def remove_book():
    pass


if __name__ == '__main__':
    init_db()
    app.run(port="5001",debug=True)
