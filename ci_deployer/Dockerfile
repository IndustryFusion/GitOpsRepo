FROM alpine/k8s:1.27.1

RUN wget https://github.com/helmfile/helmfile/releases/download/v0.154.0/helmfile_0.154.0_linux_amd64.tar.gz
RUN tar -xf helmfile_0.154.0_linux_amd64.tar.gz
RUN chmod u+x helmfile
RUN mv helmfile /usr/bin/helmfile
RUN addgroup -S deployer && adduser -S deployer -G deployer -h /home/deployer/
USER deployer
WORKDIR /home/deployer
ADD kubeconfig /home/deployer/.kube/config
ENV KUBECONFIG=/home/deployer/.kube/config