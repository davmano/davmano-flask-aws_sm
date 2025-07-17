## Project Structure 

```
.
├── app.py
├── Dockerfile
├── .github
│   └── workflows
│       └── cicd.yml
├── k8s
│   ├── argocd.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── secret.yaml
│   └── service.yaml
├── monitoring
│   ├── prometheus-grafana-argocd.yaml
│   └── values.yaml
├── README.md
├── requirements.txt
└── .trivyignore
```

## CI/CD Pipeline Badge

[![CI/CD](https://github.com/davmano/davmano-flask-aws_sm/actions/workflows/cicd.yml/badge.svg)](https://github.com/davmano/davmano-flask-aws_sm/actions/workflows/cicd.yml)
