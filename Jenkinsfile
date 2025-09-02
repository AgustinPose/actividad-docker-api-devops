pipeline {
    agent any
    stages {
        stage('Build imagen Docker') {
            steps {
                sh 'docker build -t notas-api:latest .'
            }
        }
    }
}
