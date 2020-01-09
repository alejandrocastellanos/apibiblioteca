from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
import graphene
import requests 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1602@localhost/biblioteca'
db = SQLAlchemy(app)

class Libro(db.Model):
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
    #id_servicio = db.Column(db.String(200), unique=False, nullable=True)
    
    def __repr__(self):
        return '<Titulo {}>'.format(self.titulo)

# objeto que lista todos los libros
class ListAllBooksObject(SQLAlchemyObjectType):
    class Meta:
        model = Libro
        interfaces = (graphene.relay.Node, )

#crear libro en la base de datos
class CreateBook(graphene.Mutation):
    class Arguments:
        titulo = graphene.String(required=True)
        subtitulo = graphene.String(required=True)
        autor = graphene.String(required=True)
        categoria = graphene.String(required=True)
        fecha_publicacion = graphene.String(required=True)
        editor = graphene.String(required=True)
        descripcion = graphene.String(required=True)
        imagen = graphene.String(required=True)
    
    createbook = graphene.Field(lambda: ListAllBooksObject)

    def mutate(self, info, titulo, subtitulo, autor, categoria, fecha_publicacion, editor, descripcion, imagen):
        createbook = Libro(titulo=titulo, subtitulo=subtitulo, autor=autor, categoria=categoria, fecha_publicacion=fecha_publicacion, editor=editor, descripcion=descripcion, imagen=imagen)
        db.session.add(createbook)
        db.session.commit()

        return CreateBook(createbook=createbook)

#elimianr libro por ID
class DeleteBook(graphene.Mutation):
    delete = graphene.Boolean()
    
    class Arguments:
        id = graphene.String(required=True)
    
    def mutate(cls, info, id):
        deletebook = db.session.query(Libro).filter(Libro.id==int(id)).first()
        delete = False
        if deletebook != None:
            delete = True
            
        db.session.query(Libro).filter(Libro.id==int(id)).delete()
        db.session.commit()
        return DeleteBook(delete=delete)

#crear libro de api google por ID
class RegisterGoogleBook(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)   
    
    registergooglebook = graphene.Field(lambda: ListAllBooksObject)

    def mutate(self, info, id):
        urlgooglebooks = "https://www.googleapis.com/books/v1/volumes?q={}".format(id)
        r = requests.get(urlgooglebooks)
        data = r.json()
        titulo = data["items"][0]["volumeInfo"]["title"]
        subtitulo = data["items"][0]["volumeInfo"]["subtitle"]
        autor = data["items"][0]["volumeInfo"]["authors"][0]
        try:
            categoria = data["items"][0]["volumeInfo"]["categories"][0]
        except:
            categoria = "Sin categoria"

        fecha_publicacion = data["items"][0]["volumeInfo"]["publishedDate"]        
        editor = data["items"][0]["volumeInfo"]["publisher"]
        try:
            descripcion = data["items"][0]["volumeInfo"]["description"]
        except:
            descripcion = "Sin descripción"

        imagen = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]

        registergooglebook = Libro(titulo=titulo, subtitulo=subtitulo, autor=autor, categoria=categoria, fecha_publicacion=fecha_publicacion, editor=editor, descripcion=descripcion, imagen=imagen)
        db.session.add(registergooglebook)
        db.session.commit()

        return RegisterGoogleBook(registergooglebook=registergooglebook)

#crear libro de api libros de programacion por ID
class RegisterItbookBook(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)   
    
    registeritbookbook = graphene.Field(lambda: ListAllBooksObject)

    def mutate(self, info, id):
        registeritbookbook = "https://api.itbook.store/1.0/books/{}".format(id)
        r = requests.get(registeritbookbook)
        data = r.json()

        titulo = data['title']
        subtitulo = data['subtitle']
        autor = data['authors']
        categoria = "Tecnología"
        fecha_publicacion = data["year"]
        editor = data["publisher"]
        descripcion = data["publisher"]
        imagen = data["image"]

        registeritbookbook = Libro(titulo=titulo, subtitulo=subtitulo, autor=autor, categoria=categoria, fecha_publicacion=fecha_publicacion, editor=editor, descripcion=descripcion, imagen=imagen)
        db.session.add(registeritbookbook)
        db.session.commit()

        return RegisterItbookBook(registeritbookbook=registeritbookbook)

#buscar libro en bd y en google
class SearchBookDbYGoogle(graphene.Mutation):
    titulo = graphene.String()
    subtitulo = graphene.String()
    autor = graphene.String()
    categoria = graphene.String()
    fecha_publicacion = graphene.String()
    editor = graphene.String()
    descripcion = graphene.String()
    imagen = graphene.String()

    class Arguments:
        search = graphene.String(required=True)
    
    def mutate(cls, info, search):
        searchlocaldb = db.session.query(Libro).filter(Libro.titulo==search).first()
        
        if searchlocaldb is not None:
            titulo = searchlocaldb.titulo
            subtitulo = searchlocaldb.subtitulo
            autor = searchlocaldb.autor
            categoria = searchlocaldb.categoria
            fecha_publicacion = searchlocaldb.fecha_publicacion
            editor = searchlocaldb.editor
            descripcion = searchlocaldb.descripcion
            imagen = searchlocaldb.imagen
        else:
            urlgooglebooks = "https://www.googleapis.com/books/v1/volumes?q={}".format(search)
            r = requests.get(urlgooglebooks)
            data = r.json()
            titulo = data["items"][0]["volumeInfo"]["title"]
            subtitulo = data["items"][0]["volumeInfo"]["subtitle"]
            autor = data["items"][0]["volumeInfo"]["authors"][0]
            try:
                categoria = data["items"][0]["volumeInfo"]["categories"][0]
            except:
                categoria = "Sin categoria"

            fecha_publicacion = data["items"][0]["volumeInfo"]["publishedDate"]        
            editor = data["items"][0]["volumeInfo"]["publisher"]
            try:
                descripcion = data["items"][0]["volumeInfo"]["description"]
            except:
                descripcion = "Sin descripción"

            imagen = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]

        return SearchBookDbYGoogle(titulo=titulo, subtitulo=subtitulo, autor=autor, categoria=categoria, fecha_publicacion=fecha_publicacion, editor=editor, descripcion=descripcion, imagen=imagen)


class MutationCreate(graphene.ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()
    register_google_book = RegisterGoogleBook.Field()
    register_itbook_book = RegisterItbookBook.Field()
    searchbookdbygoogle = SearchBookDbYGoogle.Field()

class Query(graphene.ObjectType):
    #listar todos los libros
    all_posts = SQLAlchemyConnectionField(ListAllBooksObject)    

schema = graphene.Schema(query=Query, mutation=MutationCreate)

app.add_url_rule(
    '/libro',
    view_func=GraphQLView.as_view(
        'libro',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
     app.run()