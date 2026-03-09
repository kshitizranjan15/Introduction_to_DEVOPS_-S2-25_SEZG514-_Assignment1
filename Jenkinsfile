pipeline {
    agent any

    environment {
        IMAGE_TAG  = "aceest:build-${env.BUILD_NUMBER}"
        VENV_DIR   = "${env.WORKSPACE}/.venv"
        REPO_OWNER = "kshitizranjan15"
        REPO_NAME  = "Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1"
        // Store your GitHub PAT as a Jenkins secret text credential with id 'github-token'
        // Manage Jenkins → Credentials → Global → Add → Secret text → ID: github-token
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_HASH = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    echo "✅ Checked out commit: ${env.GIT_COMMIT_HASH}"
                    // Post 'pending' status to GitHub commit
                    postGitHubStatus('pending', 'Jenkins build started', 'continuous-integration/jenkins')
                }
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
            script {
                postGitHubStatus('success', 'Jenkins build passed', 'continuous-integration/jenkins')
            }
        }
        failure {
            echo "❌ BUILD FAILED — check stage logs above"
            script {
                postGitHubStatus('failure', 'Jenkins build failed', 'continuous-integration/jenkins')
            }
        }
        always {
            sh 'rm -rf ${VENV_DIR} || true'
            archiveArtifacts artifacts: 'test-results/*.xml', allowEmptyArchive: true
            cleanWs()
        }
    }
}

// Helper: post a commit status to GitHub via REST API
// Requires Jenkins credential 'github-token' (secret text = GitHub PAT)
// PAT needs repo:status scope
def postGitHubStatus(String state, String description, String context) {
    try {
        withCredentials([string(credentialsId: 'github-token', variable: 'GH_TOKEN')]) {
            def commitHash = env.GIT_COMMIT_HASH ?: sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
            def payload = groovy.json.JsonOutput.toJson([
                state      : state,
                description: description,
                context    : context,
                target_url : "${env.BUILD_URL}"
            ])
            sh """
                curl -s -o /dev/null -w "GitHub status API: %{http_code}\\n" \\
                  -H "Authorization: token ${GH_TOKEN}" \\
                  -H "Content-Type: application/json" \\
                  -X POST \\
                  -d '${payload}' \\
                  "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/statuses/${commitHash}"
            """
        }
    } catch (Exception e) {
        echo "⚠️  GitHub status update skipped (no 'github-token' credential): ${e.message}"
    }
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