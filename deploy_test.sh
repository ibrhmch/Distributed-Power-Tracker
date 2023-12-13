kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml
kubectl apply -f psql/psql-deployment.yaml
kubectl apply -f psql/psql-service.yaml

sleep 5
kubectl apply -f rest-server/rest-deployment.yaml
kubectl apply -f rest-server/rest-service.yaml
kubectl apply -f rest-server/rest-ingress.yaml

sleep 5
kubectl apply -f socket/ss-deployment.yaml
kubectl apply -f socket/ss-service.yaml
# kubectl apply -f socket/ss-ingress.yaml

sleep 10
kubectl apply -f frontend/front-deployment.yaml
kubectl apply -f frontend/front-service.yaml
kubectl apply -f frontend/front-ingress.yaml

sleep 5

# while true; do kubectl port-forward svc/socket 5001:5001&; done

