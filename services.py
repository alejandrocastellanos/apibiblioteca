import requests

def ServiceGoogle(search):
    urlgooglebooks = "https://www.googleapis.com/books/v1/volumes?q={}".format(search)
    r = requests.get(urlgooglebooks)
    data = r.json()
    
    titulo = data["items"][0]["volumeInfo"]["title"]
    try:
        subtitulo = data["items"][0]["volumeInfo"]["subtitle"]
    except:
        subtitulo = "Sin datos"
    autor = data["items"][0]["volumeInfo"]["authors"][0]
    try:
        categoria = data["items"][0]["volumeInfo"]["categories"][0]
    except:
        categoria = "Sin categoria"
    fecha_publicacion = data["items"][0]["volumeInfo"]["publishedDate"]        
    try:
        editor = data["items"][0]["volumeInfo"]["publisher"]
    except:
        editor = "Sin datos"
    try:
        descripcion = data["items"][0]["volumeInfo"]["description"]
    except:
        descripcion = "Sin descripción"
    imagen = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]

    Data = {"titulo":titulo, "subtitulo":subtitulo, "autor":autor, "categoria":categoria, "fecha_publicacion":fecha_publicacion, "editor":editor, "descripcion":descripcion, "imagen":imagen}
    return Data

def ServiceItbook(search):
    registeritbookbook = "https://api.itbook.store/1.0/books/{}".format(search)
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

    Data = {"titulo":titulo, "subtitulo":subtitulo, "autor":autor, "categoria":categoria, "fecha_publicacion":fecha_publicacion, "editor":editor, "descripcion":descripcion, "imagen":imagen}
    return Data

def ServiceItbookall(search):
    registeritbookbook = "https://api.itbook.store/1.0/search/{}".format(search)
    r = requests.get(registeritbookbook)
    data = r.json()
    return data

def ServiceGoogleall(search):
    urlgooglebooks = "https://www.googleapis.com/books/v1/volumes?q={}".format(search)
    r = requests.get(urlgooglebooks)
    data = r.json()
    return data