pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
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
                sh 'python3 -m compileall -q app tests scripts'
                sh 'for script in scripts/*.sh; do bash -n "$script"; done'
            }
        }
        stage('Test') {
            steps { sh 'python3 -m unittest discover -s tests -v' }
        }
        stage('Docker Build') {
            steps {
                sh 'docker info >/dev/null'
                sh 'docker compose config --quiet'
                sh 'docker build -t "$IMAGE_NAME:$BUILD_NUMBER" .'
            }
        }
        stage('Docker Run') {
            steps {
                sh '''#!/usr/bin/env bash
set -euo pipefail
container_name="yedige-lab-ci-${BUILD_TAG}"
cleanup() { docker rm -f "$container_name" >/dev/null 2>&1 || true; }
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
docker run -d --name "$container_name" "$IMAGE_NAME:$BUILD_NUMBER"
if ! docker exec -i "$container_name" python3 - < scripts/http_smoke.py; then
    docker logs "$container_name"
    exit 1
fi
test "$(docker exec "$container_name" id -u)" != 0
'''
            }
        }
    }
    post {
        always {
            sh 'docker rm -f "yedige-lab-ci-${BUILD_TAG}" >/dev/null 2>&1 || true'
        }
    }
}
