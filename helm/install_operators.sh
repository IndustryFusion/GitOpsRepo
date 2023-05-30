#!/bin/bash

NAMESPACE="${NAMESPACE:-iff50}"

printf "\n"
printf "\033[1mCreating namespace: ${NAMESPACE}\n"
printf -- "------------------------\033[0m\n"

kubectl create ns "${NAMESPACE}"

printf "\n"
printf "\033[1mInstalling MongoDB Operator\n"
printf -- "------------------------\033[0m\n"

helm repo add mongodb https://mongodb.github.io/helm-charts
helm install community-operator mongodb/community-operator --namespace "${NAMESPACE}"

printf -- "\033[1mOperators installed successfully.\033[0m\n"