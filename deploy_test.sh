kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml
kubectl apply -f psql/psql-deployment.yaml
kubectl apply -f psql/psql-service.yaml
# kubectl apply -f nginx-deploy.yaml

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
kubectl port-forward --address 0.0.0.0 service/frontend 4999:4999 &
kubectl port-forward --address 0.0.0.0 service/rest 5000:5000 &
# while true; do kubectl port-forward svc/socket 5001:5001&; done

