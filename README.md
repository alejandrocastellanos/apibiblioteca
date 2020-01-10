# apibiblioteca
Api que exponé URLs para consultar, registrar y eliminar datos sobre libros.

# Url
  - http://

# Enpoints
  - /registrar-google-libro
  - /registrar-itbook-libro
  - /eliminar-libro
  - /buscar-libro-db-google
  - /buscar-libro-db-itbook

# Headers
  - X-Api-Key 1234abcd
  - Content-Type application/json

# Metodos y Json por Endpoint
```sh
endpoint = /registrar-google-libro
json = {"id":"id libro google"} (ejemplo: {"id":"9781484206485"})
method = POST
```

```sh
endpoint = /registrar-itbook-libro
json = {"id":"id libro google"} (ejemplo: {"id":"9781484206485"})
method = POST
```

```sh
endpoint = /eliminar-libro
json = {"id":"id de la bd"} (ejemplo: {"id":"6"})
method = DELETE
```

```sh
endpoint = /buscar-libro-db-google
json = {"search":"buscar libro por cualquier atributo"} (ejemplo: {"search":"Python 3"})
method = POST
```

```sh
endpoint = /buscar-libro-db-itbook
json = {"search":"buscar libro por cualquier atributo"} (ejemplo: {"search":"javascript"})
method = POST
```