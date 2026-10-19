pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
    }
    environment {
        IMAGE_NAME = 'yedige-batyrkhan-devops'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build') {
            steps {
                sh 'python3 -m compileall -q app tests'
                sh 'for script in scripts/*.sh; do bash -n "$script"; done'
            }
        }
        stage('Test') {
            steps { sh 'python3 -m unittest discover -s tests -v' }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t "$IMAGE_NAME:$BUILD_NUMBER" .' }
        }
        stage('Docker Run') {
            steps {
                sh '''#!/usr/bin/env bash
set -euo pipefail
container_id=$(docker run -d "$IMAGE_NAME:$BUILD_NUMBER")
cleanup() { docker rm -f "$container_id" >/dev/null 2>&1 || true; }
trap cleanup EXIT
for attempt in {1..30}; do
    if docker exec "$container_id" python3 -c "import json, urllib.request; data=json.load(urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)); assert data['status']=='ok'"; then
        exit 0
    fi
    sleep 1
done
docker logs "$container_id"
exit 1
'''
            }
        }
    }
}
