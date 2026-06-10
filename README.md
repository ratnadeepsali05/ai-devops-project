# ai-devops-project [https://chatgpt.com/canvas/shared/6a0f016c122081919347b5e3ec39b491]

#Step 1 — Install Docker

 -**Ubuntu Installation**
   sudo apt update
   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker

- Verify
  docker --version

#Step 2 — Install Minikube
- Install kubectl
  curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes release/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x kubectl
  sudo mv kubectl /usr/local/bin/

- Install Minikube
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube

- Start Cluster
  minikube start --driver=docker --force

- Verify Cluster
  kubectl get nodes

#Step 3 — Application Development
- Create Application Directory
  mkdir -p ai-devops-project/app
  cd ai-devops-project/app

- Flask Application Code
  app.py

from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "AI DevOps Monitoring Project Running Successfully"

@app.route('/health')
def health():
    return {
        "status": "healthy"
    }

@app.route('/error')
def error():
    errors = [
        "Database Connection Timeout",
        "Memory Overflow Detected",
        "Application Crash",
        "High CPU Usage"
    ]

    return {
        "error": random.choice(errors)
    }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

- Python Requirements
  requirements.txt
   flask

- Dockerization
  Dockerfile

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]

- Build Docker Image

  docker build -t ai-devops-app:v1 .

- Run Docker Container

  docker run -d -p 5000:5000 ai-devops-app:v1

#Step 4 — Kubernetes Deployment

- deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-devops-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ai-devops-app

  template:
    metadata:
      labels:
        app: ai-devops-app

    spec:
      containers:
      - name: ai-devops-app
        image: ai-devops-app:v1
        imagePullPolicy: Never

        ports:
        - containerPort: 5000

        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"

          limits:
            memory: "256Mi"
            cpu: "200m"

- service.yaml

apiVersion: v1
kind: Service
metadata:
  name: ai-devops-service
spec:
  selector:
    app: ai-devops-app

  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000

  type: NodePort

- Deploy Application
  kubectl apply -f deployment.yaml
  kubectl apply -f service.yaml

- Verify Deployment
  kubectl get pods
  kubectl get svc

- Access Application
  minikube service ai-devops-service

#Step 5 — Jenkins CI/CD Pipeline

- Install Jenkins Using Docker
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

- Jenkinsfile
pipeline {
    agent any

    environment {
        IMAGE_NAME = "ai-devops-app:v1"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-repo/ai-devops-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME ./app'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f kubernetes/'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get pods'
            }
        }
    }
}

#Step 6 — Install Monitoring Stack

- Add Helm Repositories

  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  helm repo add grafana https://grafana.github.io/helm-charts
  helm repo update

- Install Prometheus
  helm install prometheus prometheus-community/prometheus

- Install Grafana
  helm install grafana grafana/grafana

- Get Grafana Password
  kubectl get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode

- Port Forward Grafana
  kubectl port-forward service/grafana 3000:80

Access: http://localhost:3000

Username:admin

#Step 7 — Install Loki
  helm repo add grafana https://grafana.github.io/helm-charts
  helm install loki grafana/loki-stack

- Verify Loki
  kubectl get pods

#Step 8 — Configure Alert Rules

- prometheus-alert-rules.yaml

groups:
- name: kubernetes-alerts

  rules:

  - alert: HighCPUUsage
    expr: sum(rate(container_cpu_usage_seconds_total[1m])) > 0.8
    for: 1m

    labels:
      severity: critical

    annotations:
      summary: "High CPU Usage Detected"
      description: "Container CPU usage exceeded threshold"

  - alert: PodRestarting
    expr: kube_pod_container_status_restarts_total > 3
    for: 1m

    labels:
      severity: warning

    annotations:
      summary: "Pod Restarting Frequently"
      description: "Pod restart count exceeded threshold"

#Step 9 — Install Ollama
- Linux Installation
  curl -fsSL https://ollama.com/install.sh | sh

- Pull Llama3 Model
  ollama pull llama3

- Run Llama3
 ollama run llama3

#Step 10 — AI Log Analyzer

Install Python Dependencies

- ai-engine/requirements.txt
  requests

#AI Prompt

- prompt.txt

Analyze the Kubernetes incident logs.
Provide:
1. Root Cause
2. Severity
3. Suggested Remediation
4. Short Incident Summary

- analyzer.py

import requests
import json
import subprocess

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def get_pod_logs():

    command = [
        "kubectl",
        "logs",
        "deployment/ai-devops-app"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout


def analyze_logs(logs):

    prompt = f"""
    Analyze Kubernetes logs.

    Logs:
    {logs}

    Explain:
    - Root cause
    - Severity
    - Remediation
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    data = response.json()

    return data['response']


if __name__ == '__main__':

    logs = get_pod_logs()

    analysis = analyze_logs(logs)

    print("\n===== AI ANALYSIS =====\n")

    print(analysis)

- Execute AI Analyzer
   python analyzer.py

#Step 11 — Slack Integration

- Create Slack Incoming Webhook

- Go to Slack:
  Apps → Incoming Webhooks → Activate Webhooks
  Copy webhook URL.

- slack_alert.py
import requests
import json

SLACK_WEBHOOK = "YOUR_SLACK_WEBHOOK_URL"


def send_slack_alert(message):

    payload = {
        "text": message
    }

    requests.post(
        SLACK_WEBHOOK,
        data=json.dumps(payload)
    )


if __name__ == '__main__':

    message = "AI Incident Analysis Completed Successfully"

    send_slack_alert(message)

#Step 12 — Auto Remediation
- auto_remediation.py
import subprocess


def restart_deployment():

    command = [
        "kubectl",
        "rollout",
        "restart",
        "deployment/ai-devops-app"
    ]

    subprocess.run(command)


if __name__ == '__main__':

    restart_deployment()

    print("Deployment restarted successfully")

- Simulating Failures

 - Generate Errors

  - Open: http://localhost/error

T  his triggers logs and alerts.

#Monitoring Dashboards

- Grafana Dashboards

- Monitor:
 CPU usage
 Memory usage
 Pod restarts
 Request count
 Error rate
 Cluster health



- Important Kubernetes Commands

- Check Pods
  kubectl get pods

- Describe Pod
  kubectl describe pod <pod-name>

- Check Logs
  kubectl logs <pod-name>

- Restart Deployment
  kubectl rollout restart deployment ai-devops-app
    
