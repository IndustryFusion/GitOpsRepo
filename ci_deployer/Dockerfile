FROM alpine/k8s:1.27.1

RUN apk add --no-cache --update --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing helmfile 

RUN addgroup -S deployer && adduser -S deployer -G deployer -h /home/deployer/
USER deployer
WORKDIR /home/deployer
ADD kubeconfig /home/deployer/.kube/config
ENV KUBECONFIG=/home/deployer/.kube/config