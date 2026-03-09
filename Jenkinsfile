pipeline {
    agent any

    environment {
        // Tag the image with the Jenkins build number for traceability
        IMAGE_TAG = "aceest:build-${env.BUILD_NUMBER}"
        VENV_DIR  = "${env.WORKSPACE}/.venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo "✅ Checked out branch: ${env.GIT_BRANCH ?: 'local'}"
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip --quiet
                    ${VENV_DIR}/bin/pip install -r requirements.txt --quiet
                    echo "✅ Python virtualenv ready"
                    ${VENV_DIR}/bin/python --version
                '''
            }
        }

        stage('Lint / Syntax Check') {
            steps {
                sh '''
                    ${VENV_DIR}/bin/python -m compileall . -q
                    echo "✅ Syntax check passed"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    ${VENV_DIR}/bin/pytest -q \
                        --tb=short \
                        --junitxml=test-results/results.xml
                    echo "✅ All tests passed"
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results/results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_TAG} .
                    docker tag ${IMAGE_TAG} aceest:latest
                    echo "✅ Docker image built: ${IMAGE_TAG}"
                '''
            }
        }

        stage('Test Inside Container') {
            steps {
                sh '''
                    docker run --rm ${IMAGE_TAG} pytest -q
                    echo "✅ Container-level tests passed"
                '''
            }
        }

    }

    post {
        success {
            echo "🎉 BUILD SUCCESS — image: ${IMAGE_TAG}"
        }
        failure {
            echo "❌ BUILD FAILED — check stage logs above"
        }
        always {
            // Clean up the virtualenv to keep workspace tidy
            sh 'rm -rf ${VENV_DIR} || true'
            archiveArtifacts artifacts: 'test-results/*.xml', allowEmptyArchive: true
            cleanWs()
        }
    }
}