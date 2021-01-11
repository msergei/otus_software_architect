# otus_software_architect
Software arhitect course, homework 1

### URL

http://simple-service.default.svc.cluster.local

default - default namespace

### How to get response outside cluster?

- get ingress ip and port via:
```kubectl get ingress```

- set ip to /etc/hosts (sudo needed):
```echo 'IP arch.homework' >> /etc/hosts```

- send request
```curl http://arch.homework/otusapp/username/health```

### How to get response directrly to service inside node?

- get pod ip via:
```kubectl get services```

- send request
```curl http://POD-IP:8000/health```

### How to run postman tests with newman?
newman run homework1.postman_collection.json


