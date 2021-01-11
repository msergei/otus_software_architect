# otus_software_acrhitect
Software arhitect course, homework 4

# minikube install
```shell script
minikube start \
--cpus=4 --memory=5g \
--cni=flannel \
--extra-config=apiserver.enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,\
DefaultTolerationSeconds,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota,PodPreset \
--extra-config=apiserver.authorization-mode=Node,RBAC
```

# Jaeger install
```shell script
helm install -n jaeger-operator --create-namespace -f jaeger/operator-values.yaml jaeger-operator jaegertracing/jaeger-operator
kubectl apply -f jaeger/jaeger.yaml
kubectl get po -n jaeger -l app.kubernetes.io/instance=jaeger
```

### Jaeger port forward

```shell script
minikube service -n jaeger jaeger-query-nodeport
```

# Prometheus install

```shell script
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update
```

### Deploy prom

```shell script
helm install --version "9.4.4" -n monitoring --create-namespace -f prometheus/operator-values.yaml prometheus prometheus-community/kube-prometheus-stack
kubectl apply -f prometheus/monitoring-nodeport.yaml
kubectl get po -n monitoring
```

### Port forward:

```shell script
minikube service -n monitoring prometheus-grafana-nodeport
minikube service -n monitoring prom-prometheus-nodeport
```

# Istio install

```shell script
istioctl install --set profile=demo
kubectl label namespace default istio-injection=enabled
kubectl apply -f istio/istio.yaml
kubectl get all -n istio-system -l istio.io/rev=default
```

## Kiali install

```shell script
helm repo add kiali https://kiali.org/helm-charts
helm repo update
helm install -n kiali-operator --create-namespace kiali-operator kiali/kiali-operator
kubectl apply -f kiali/kiali.yaml
```

## Kiali port-forward

```shell script
minikube service -n kiali kiali-nodeport
```
# build
```shell script
eval $(minikube docker-env) && docker build -t proxy-app:latest -f app/src/Dockerfile app/src
```

# echoserver up
```shell script
kubectl apply -f app/echoserver.yaml
kubectl get po -l "app=echoserver"
minikube service echoserver
```

#proxy-app up
```shell script
kubectl apply -f app/proxy-app.yaml
kubectl get po -l "app=proxy-app"
minikube service proxy-app
```

## Test echo & proxy
```shell script
curl "http://127.0.0.1:50200?url=http://echoserver"
```

### disable

```shell script
kubectl apply -f manage-traffic/proxy-network-disable.yaml
```

```shell script
curl "http://127.0.0.1:50200?url=http://echoserver"
```

### enable

```shell script
kubectl apply -f manage-traffic/proxy-network-enable.yaml
```

```shell script
curl "http://127.0.0.1:50200?url=http://echoserver"
```

## Auth test

```shell script
kubectl apply -f auth/echoserver-auth-enable.yaml
curl "http://127.0.0.1:50200?url=http://echoserver"
```

```shell script
curl -H "X-AUTH-TOKEN: token" "http://127.0.0.1:50200?url=http://echoserver"
```

### enable token adding
```shell script
kubectl apply -f auth/proxy-auth-enable.yaml
```
```shell script
curl "http://127.0.0.1:50200?url=http://echoserver"
```

## Retries test

```shell script
curl "http://127.0.0.1:50200?url=http://echoserver/error?times=3"
```
```shell script
kubectl apply -f retries/echoserver-retries-enbale.yamls
```

```shell script
curl "http://127.0.0.1:50200?url=http://echoserver/error?times=3"
```



# Balancing install

```shell script
kubectl label namespace default istio-injection=enabled
kubectl apply -f balancing/deployment.yml
```

## Check app works
```shell script
kubectl port-forward service/website 8000:80
```

## Apply istio balancing
```shell script
kubectl apply -f balancing/website-routing.yaml
```

## Port forward to istio ingress
```shell script
kubectl port-forward service/istio-ingressgateway -n istio-system 8000:80
```

## Try to open:
```shell script
curl "http://127.0.0.1:8000/"
```

## Let's open Kiali console to see graph
```shell script
kubectl port-forward service/kiali-nodeport -n kiali 8080:20001
```