from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

import graphene

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
    descripcion = db.Column(db.String(500), unique=False, nullable=False)
    imagen = db.Column(db.String(700), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Titulo {}>'.format(self.titulo)

# Schema Objects
class ListAllBooksObject(SQLAlchemyObjectType):
    class Meta:
        model = Libro
        interfaces = (graphene.relay.Node, )

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
    ok = graphene.Boolean()
    
    class Arguments:
        id = graphene.String(required=True)
    
    def mutate(cls, info, id):
        deletebook = db.session.query(Libro).filter(Libro.id==int(id)).first()
        if deletebook != None:
            ok = True
        else:
            ok = False
        db.session.query(Libro).filter(Libro.id==int(id)).delete()
        db.session.commit()
        return DeleteBook(ok=ok)

class MutationCreate(graphene.ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    #listar todos los libros
    all_posts = SQLAlchemyConnectionField(ListAllBooksObject)    
    #buscar libro
    get_book = graphene.Field(lambda: ListAllBooksObject, search=graphene.String())
    def resolve_get_book(parent, info, search):
        query = ListAllBooksObject.get_query(info)
        result = query.filter(Libro.titulo == search).first()
        return result

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


#crear nuevo libro
#newbook = Libro(titulo="prueba", autor="prueba2") 
#db.session.add(newbook) 
#db.session.commit()

#listar libros por valor
#searchbook = Libro.query.filter_by(autor='prueba2').first()
#print(searchbook.id)
