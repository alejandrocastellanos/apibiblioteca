from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1602@localhost/biblioteca'
db = SQLAlchemy(app)

class Libro(db.Model):
    __tablename__ = 'libro'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), unique=True, nullable=False)
    autor = db.Column(db.String(200), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Autor {}>'.format(self.autor)

#crear nuevo libro
#newbook = Libro(titulo="prueba", autor="prueba2") 
#db.session.add(newbook) 
#db.session.commit()

#listar libros por valor
searchbook = Libro.query.filter_by(autor='prueba2').first()
print(searchbook.id)