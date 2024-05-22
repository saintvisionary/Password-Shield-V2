password-shield/
│
├── api/
│   ├── __init__.py
│   ├── auth.py
│   ├── hash_cracker.py
│   ├── models.py
│   ├── resources.py
│   ├── utils.py
│   └── graphql_schema.py
│
├── services/
│   ├── blockchain_service.py
│   ├── federated_learning_service.py
│   ├── serverless_functions.py
│   ├── hash_service.py
│   ├── monitoring_service.py
│   └── wordlist_service.py
│
├── ml/
│   ├── gpt2_model.py
│   └── lstm_model.py
│
├── ui/
│   ├── public/
│   ├── src/
│   └── package.json
│
├── infra/
│   ├── istio-config.yaml
│   ├── kubernetes/
│   └── terraform/
│
├── ci-cd/
│   ├── jenkinsfile
│   ├── github_actions.yml
│   └── docker-compose.ci.yml
│
├── data/
│   └── spark/
│
├── logs/
│   └── fluentd/
│
├── Dockerfile
├── docker-compose.yml
├── main.py
└── requirements.txt
