# otus_software_acrhitect
Software arhitect course, homework 2

### URLs

```
POST http://arch.homework/otusapp/mironov/api/v1/users/
GET http://arch.homework/otusapp/mironov/api/v1/users/<id>/
PATCH http://arch.homework/otusapp/mironov/api/v1/users/<id>/
DELETE http://arch.homework/otusapp/mironov/api/v1/users/<id>/
```

### How to deploy chart?

```helm install myapp ./crud-chart```


### How to run postman tests with newman?
```newman run homework2.postman_collection.json```
