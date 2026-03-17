# Secret Management

Sample code to handle secret management across various cloud providers.

```
# ============================================================
# bootstrap/external-secrets-setup.yaml
# Cloud-agnostic External Secrets + cert-manager bootstrap
#
# Supported backends (set provider.type below):
#   - aws          → AWS Secrets Manager (GovCloud or standard)
#   - azure        → Azure Key Vault
#   - gcp          → GCP Secret Manager
#   - vault        → HashiCorp Vault
#   - kubernetes   → Kubernetes Secrets (air-gapped / local)
# ============================================================

---
# Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: convai-system
  labels:
    kubernetes.io/metadata.name: convai-system
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# ============================================================
# PROVIDER CONFIGURATION
# Uncomment exactly ONE SecretStore block below.
# All ExternalSecret resources reference "convai-secret-store"
# by name, so swapping providers requires no changes downstream.
# ============================================================

# ------------------------------------------------------------
# OPTION A: AWS Secrets Manager (with IRSA)
# ------------------------------------------------------------
# apiVersion: external-secrets.io/v1beta1
# kind: SecretStore
# metadata:
#   name: convai-secret-store
#   namespace: convai-system
# spec:
#   provider:
#     aws:
#       service: SecretsManager
#       region: us-gov-west-1          # change to your region
#       auth:
#         jwt:
#           serviceAccountRef:
#             name: convai-eso-sa      # IRSA-annotated SA below

# ------------------------------------------------------------
# OPTION B: Azure Key Vault (with Workload Identity)
# ------------------------------------------------------------
# apiVersion: external-secrets.io/v1beta1
# kind: SecretStore
# metadata:
#   name: convai-secret-store
#   namespace: convai-system
# spec:
#   provider:
#     azurekv:
#       tenantId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
#       vaultUrl: "https://convai-keyvault.vault.azure.net"
#       authType: WorkloadIdentity
#       serviceAccountRef:
#         name: convai-eso-sa

# ------------------------------------------------------------
# OPTION C: GCP Secret Manager (with Workload Identity)
# ------------------------------------------------------------
# apiVersion: external-secrets.io/v1beta1
# kind: SecretStore
# metadata:
#   name: convai-secret-store
#   namespace: convai-system
# spec:
#   provider:
#     gcpsm:
#       projectID: "your-gcp-project-id"
#       auth:
#         workloadIdentity:
#           clusterLocation: us-central1
#           clusterName: convai-cluster
#           serviceAccountRef:
#             name: convai-eso-sa

# ------------------------------------------------------------
# OPTION D: HashiCorp Vault (token or Kubernetes auth)
# ------------------------------------------------------------
# apiVersion: external-secrets.io/v1beta1
# kind: SecretStore
# metadata:
#   name: convai-secret-store
#   namespace: convai-system
# spec:
#   provider:
#     vault:
#       server: "https://vault.internal.agency.gov"
#       path: "secret"
#       version: "v2"
#       auth:
#         kubernetes:
#           mountPath: "kubernetes"
#           role: "convai-role"
#           serviceAccountRef:
#             name: convai-eso-sa

# ------------------------------------------------------------
# OPTION E: Kubernetes Secrets (air-gapped / dev / local)
# Reads from Secrets already present in convai-system namespace.
# Create them manually or via sealed-secrets / SOPS.
# ------------------------------------------------------------
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: convai-secret-store
  namespace: convai-system
spec:
  provider:
    kubernetes:
      remoteNamespace: convai-system
      server:
        caProvider:
          type: ConfigMap
          name: kube-root-ca.crt
          key: ca.crt
      auth:
        serviceAccount:
          name: convai-eso-sa

---
# ServiceAccount used by ESO to authenticate to the secret backend.
# Annotate this SA with your cloud provider's workload identity mechanism:
#
#   AWS IRSA:              eks.amazonaws.com/role-arn: "arn:aws[-us-gov]:iam::<account>:role/<role>"
#   Azure Workload ID:     azure.workload.identity/client-id: "<client-id>"
#   GCP Workload Identity: iam.gke.io/gcp-service-account: "<sa>@<project>.iam.gserviceaccount.com"
#   Vault / k8s:           no annotation needed — uses in-cluster RBAC below
apiVersion: v1
kind: ServiceAccount
metadata:
  name: convai-eso-sa
  namespace: convai-system
  annotations: {}
  # Uncomment the relevant annotation for your provider:
  # eks.amazonaws.com/role-arn: "arn:aws-us-gov:iam::123456789012:role/convai-eso-role"
  # azure.workload.identity/client-id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  # iam.gke.io/gcp-service-account: "convai-eso@my-project.iam.gserviceaccount.com"

---
# RBAC for Option E (Kubernetes provider) — not needed for cloud backends
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: convai-eso-secret-reader
  namespace: convai-system
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: convai-eso-secret-reader-binding
  namespace: convai-system
subjects:
  - kind: ServiceAccount
    name: convai-eso-sa
    namespace: convai-system
roleRef:
  kind: Role
  name: convai-eso-secret-reader
  apiGroup: rbac.authorization.k8s.io


```
