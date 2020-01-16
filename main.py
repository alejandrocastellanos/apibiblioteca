import requests
import json
import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from services import ServiceGoogle, ServiceItbook, ServiceItbookall, ServiceGoogleall

password = '1234abcd'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zkmwkdoeydfnsx:fc83a8526f265b18e58b35f9e71e5bbdbd82764bebd8b730558c023e6f569130@ec2-174-129-33-2.compute-1.amazonaws.com:5432/dck0t7jn2rfv3g'
api = Api(app)
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'libro'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), unique=False, nullable=False)
    subtitulo = db.Column(db.String(200), unique=False, nullable=False)
    autor = db.Column(db.String(200), unique=False, nullable=False)
    categoria = db.Column(db.String(200), unique=False, nullable=False)
    fecha_publicacion = db.Column(db.String(100), unique=False, nullable=False)
    editor = db.Column(db.String(100), unique=False, nullable=False)
    descripcion = db.Column(db.String(), unique=False, nullable=False)
    imagen = db.Column(db.String(700), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Titulo {}>'.format(self.titulo)

def SearchBook(search):
    return Book.query.filter((Book.titulo.match("%"+search+"%")) | (Book.subtitulo.match("%"+search+"%")) | (Book.autor.match("%"+search+"%")) | (Book.categoria.match("%"+search+"%")) | (Book.fecha_publicacion.match("%"+search+"%")) | (Book.editor.match("%"+search+"%")) | (Book.descripcion.match("%"+search+"%")) | (Book.imagen.match("%"+search+"%"))).all()

#crear libro de api google por ID
class RegisterGoogleBook(Resource):
    def post(self):
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == password:
            data_json = request.json
            try:
                id = data_json["id"]
                servicegoogle = ServiceGoogle(id)
                registergooglebook = Book(titulo=servicegoogle['titulo'], subtitulo=servicegoogle['subtitulo'], autor=servicegoogle['autor'], categoria=servicegoogle['categoria'], fecha_publicacion=servicegoogle['fecha_publicacion'], editor=servicegoogle['editor'], descripcion=servicegoogle['descripcion'], imagen=servicegoogle['imagen'])
                db.session.add(registergooglebook)
                db.session.commit()    
                result = {"Resultado":"Creado Correctamente", "id":registergooglebook.id}         
            except Exception as e:
                result = {"Resultado":"Datos incorrectos", "Descripcion":str(e)}
            return result
        else:
            return {"message": "ERROR: Unauthorized"}, 401

#crear libro de api libros de programacion por ID
class RegisterItbookBook(Resource):
    def post(self):
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == password:
            data_json = request.json
            try:
                id = data_json["id"]
                serviceitbook = ServiceItbook(id)
                registeritbookbook = Book(titulo=serviceitbook['titulo'], subtitulo=serviceitbook['subtitulo'], autor=serviceitbook['autor'], categoria=serviceitbook['categoria'], fecha_publicacion=serviceitbook['fecha_publicacion'], editor=serviceitbook['editor'], descripcion=serviceitbook['descripcion'], imagen=serviceitbook['imagen'])
                db.session.add(registeritbookbook)
                db.session.commit()

                result = {"Resultado":"Creado Correctamente", "Id":registeritbookbook.id}
            except Exception as e:
                result = {"Resultado":"Datos incorrectos", "Descripcion":str(e)}
            return result
        else:
            return {"message": "ERROR: Unauthorized"}, 401

#eliminar libro
class DeleteBook(Resource):
    def delete(delf):
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == password:
            data_json = request.json
            try:
                id = data_json["id"]
                deletebook = db.session.query(Book).filter(Book.id==int(id)).first()
                result = {"Resultado":"El id no existe"}
                if deletebook != None:
                    db.session.query(Book).filter(Book.id==int(id)).delete()
                    db.session.commit()
                    result = {"Resultado":"Eliminado Correctamente"}
            except Exception as e:
                result = {"Resultado":"Datos incorrectos", "Descripcion":str(e)}
            return result
        else:
            return {"message": "ERROR: Unauthorized"}, 401

#buscar libro en db y en google books
class SearchBookDbYGoogle(Resource):
    def post(delf):
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == password:
            data_json = request.json
            try:
                search = data_json["search"] 

                queryfilter = SearchBook(search)

                if len(queryfilter) > 0:
                    resultbooks = []
                    for x in range(0, len(queryfilter)):
                        book = {"id":queryfilter[x].id, "titulo":queryfilter[x].titulo, "subtitulo":queryfilter[x].subtitulo, "autor":queryfilter[x].autor, "categoria":queryfilter[x].categoria, "fecha_publicacion":queryfilter[x].fecha_publicacion, "editor":queryfilter[x].editor, "descripcion":queryfilter[x].descripcion, "imagen":queryfilter[x].imagen}
                        resultbooks.append(book)
                    result = {"Resultado": resultbooks}
                else:
                    searchGoogleBooks = ServiceGoogleall(search)
                    result = {"Resultado": searchGoogleBooks}
            except Exception as e:
                result = {"Resultado":"Error", "Descripcion":str(e)}
            return result
        else:
            return {"message": "ERROR: Unauthorized"}, 401

#buscar libro en db y en itbooks
class SearchBookDbYItbook(Resource):
    def post(delf):
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == password:
            data_json = request.json
            try:
                search = data_json["search"] 
                queryfilter = SearchBook(search)
                print(queryfilter)
                if len(queryfilter) > 0:
                    resultbooks = []
                    for x in range(0, len(queryfilter)):
                        book = {"id":queryfilter[x].id, "titulo":queryfilter[x].titulo, "subtitulo":queryfilter[x].subtitulo, "autor":queryfilter[x].autor, "categoria":queryfilter[x].categoria, "fecha_publicacion":queryfilter[x].fecha_publicacion, "editor":queryfilter[x].editor, "descripcion":queryfilter[x].descripcion, "imagen":queryfilter[x].imagen}
                        resultbooks.append(book)
                    result = {"Resultado": resultbooks}
                else:
                    searchItBooks = ServiceItbookall(search)
                    result = {"Resultado": searchItBooks}
            except Exception as e:
                result = {"Resultado":"Error", "Descripcion":str(e)}
            return result, 200
        else:
            return {"message": "ERROR: Unauthorized"}, 401

api.add_resource(RegisterGoogleBook, '/registrar-google-libro')   
api.add_resource(RegisterItbookBook, '/registrar-itbook-libro')
api.add_resource(DeleteBook, '/eliminar-libro')
api.add_resource(SearchBookDbYGoogle, '/buscar-libro-db-google')
api.add_resource(SearchBookDbYItbook, '/buscar-libro-db-itbook')

#if __name__ == '__main__':
#    app.run(debug=True, host='localhost', port=8080)