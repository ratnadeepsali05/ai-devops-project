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