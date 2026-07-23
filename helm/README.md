# XANA — Rancher Fleet charts

Each service is its own self-contained Helm chart + Fleet bundle, one folder
per deployable workload:

```
helm/charts/
├── mongo/               # in-cluster MongoDB
├── qdrant/               # in-cluster vector store
├── backend/               # NestJS API (+ optional connector-seed Job)
├── frontend/               # Next.js UI
├── workflow-agent/       # LangGraph / FastAPI agent
├── web-connector/         # web/wiki knowledge connector
├── dynamics-connector/     # Dynamics CRM connector
├── ollama/                 # in-cluster Ollama server (vision captioning)
└── ovms/                   # in-cluster OpenVINO Model Server (alt. vision-captioning backend)
```

Every chart follows the same layout: `Chart.yaml`, `values.yaml`,
`fleet.yaml`, `templates/`. All charts share the same `defaultNamespace:
xana` in their `fleet.yaml`, and every Service is given a **fixed, non
release-prefixed name** (`mongo`, `qdrant`, `backend`, ...) so charts can
reach each other over stable in-cluster DNS regardless of which Helm
release name Fleet assigns each bundle — e.g. the backend chart's default
`config.mongodbUri` is `mongodb://mongo:27017/xana-business`.

## Rancher GitRepo configuration

In Continuous Delivery, the GitRepo's **Paths** must list every chart
folder explicitly (Fleet does not glob-expand a parent directory into
multiple bundles):

```
helm/charts/mongo
helm/charts/qdrant
helm/charts/backend
helm/charts/frontend
helm/charts/workflow-agent
helm/charts/web-connector
helm/charts/dynamics-connector
helm/charts/ollama
helm/charts/ovms
```

Each path becomes its own Bundle, named `<gitrepo-name>-<last-path-segment>`
(e.g. `xana-business-backend`). Do **not** also add a blank/root path —
there's no chart at the repo root, and Fleet will create a pointless empty
bundle for it.

Deploy order doesn't matter for install (envFrom only needs the ConfigMap/
Secret objects to exist, not the pods they describe to be Ready), but for a
fully working stack you generally want datastores up first:
`mongo`, `qdrant` → `backend`, `workflow-agent` → `frontend` →
`web-connector` / `dynamics-connector` (only if you need those connectors).
`ollama` and/or `ovms` can deploy independently at any point — workflow-agent
only actually calls out to whichever one `config.ollamaBaseUrl` points at,
and only if `config.visionCaptionEnabled` is `"true"`.

## Secrets

Every chart's `values.yaml` ships with placeholder/empty secret values
(`CHANGE_ME`, `""`). **Never commit real credentials.** Supply real values
either via:

- Rancher's per-target **"Helm Values"** field in the Continuous Delivery
  UI (see the commented `targetCustomizations` example in each chart's
  `fleet.yaml`), or
- `helm install <chart> ./helm/charts/<chart> --set secrets.x=...` /
  `-f my-local-secrets.yaml` for manual/local installs.

## Images

`backend`, `frontend`, `workflow-agent`, `web-connector`, and
`dynamics-connector` are custom-built images (`imageRegistry` +
`image` in each chart's `values.yaml`, default registry `ibn40/`).
`mongo`, `qdrant`, `ollama`, and `ovms` use public upstream images and
ignore `imageRegistry` — they are not part of the xana-build-deploy
image-tag-patching automation.

Build and push from the `xana-dev` monorepo:

```
./deployment/build-and-push.sh ibn40
```

## Manual install (no Fleet)

```
helm install mongo ./helm/charts/mongo -n xana --create-namespace
helm install qdrant ./helm/charts/qdrant -n xana
helm install backend ./helm/charts/backend -n xana --set secrets.appEncryptionKey=$(openssl rand -hex 32) --set secrets.adminPassword=... --set secrets.authSecret=...
helm install frontend ./helm/charts/frontend -n xana
helm install workflow-agent ./helm/charts/workflow-agent -n xana --set secrets.openaiCompatibleApiKey=... --set secrets.openaiCompatibleBaseUrl=...
# optional:
helm install web-connector ./helm/charts/web-connector -n xana --set secrets.wikiUsername=... --set secrets.wikiPassword=...
helm install dynamics-connector ./helm/charts/dynamics-connector -n xana --set secrets.crmUrl=... --set secrets.crmUsername=... --set secrets.crmPassword=...
# vision-captioning backend (pick one — workflow-agent's config.ollamaBaseUrl
# decides which is actually used; both can coexist):
helm install ollama ./helm/charts/ollama -n xana
helm install ovms ./helm/charts/ovms -n xana
```
