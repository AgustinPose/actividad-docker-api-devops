pipeline {
    agent any

    environment {
        IMAGE_NAME = 'notas-api'
        IMAGE_TAG = 'v1'  // o 'v2'
    }

    stages {
        stage('Build imagen Docker') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Aplicar en Kubernetes') {
            steps {
                bat "kubectl apply -f k8s/notas-app.yaml"
            }
        }
    }
}
