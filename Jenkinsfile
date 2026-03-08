pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pytest -q'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t aceest:jenkins .'
            }
        }

        // Optional: push to registry or deploy
    }

    post {
        always {
            junit '**/test-results/*.xml' // if you generate JUnit files in pytest, configure accordingly
            archiveArtifacts artifacts: '**/target/*.log', allowEmptyArchive: true
        }
    }
}
