pipeline {
    agent any

    environment {
        IMAGE_TAG  = "aceest:build-${env.BUILD_NUMBER}"
        VENV_DIR   = "${env.WORKSPACE}/.venv"
        REPO_OWNER = "kshitizranjan15"
        REPO_NAME  = "Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_HASH = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    echo "Checked out commit: ${env.GIT_COMMIT_HASH}"
                    postGitHubStatus('pending', 'Jenkins build started', 'continuous-integration/jenkins')
                }
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    $VENV_DIR/bin/pip install --upgrade pip --quiet
                    $VENV_DIR/bin/pip install -r requirements.txt --quiet
                    $VENV_DIR/bin/python --version
                    echo "Python virtualenv ready"
                '''
            }
        }

        stage('Lint / Syntax Check') {
            steps {
                sh '''
                    $VENV_DIR/bin/python -m compileall . -q
                    echo "Syntax check passed"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    $VENV_DIR/bin/pytest -q \
                        --tb=short \
                        --junitxml=test-results/results.xml
                    echo "All tests passed"
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
                    docker build -t $IMAGE_TAG .
                    docker tag $IMAGE_TAG aceest:latest
                    echo "Docker image built: $IMAGE_TAG"
                '''
            }
        }

        stage('Test Inside Container') {
            steps {
                sh '''
                    docker run --rm $IMAGE_TAG pytest -q
                    echo "Container-level tests passed"
                '''
            }
        }

    }

    post {
        success {
            echo "BUILD SUCCESS - image: ${IMAGE_TAG}"
            script {
                postGitHubStatus('success', 'Jenkins build passed', 'continuous-integration/jenkins')
            }
        }
        failure {
            echo "BUILD FAILED - check stage logs above"
            script {
                postGitHubStatus('failure', 'Jenkins build failed', 'continuous-integration/jenkins')
            }
        }
        always {
            sh 'rm -rf $VENV_DIR || true'
            archiveArtifacts artifacts: 'test-results/*.xml', allowEmptyArchive: true
            cleanWs()
        }
    }
}

// Posts commit status to GitHub via REST API.
// Requires Jenkins credential ID 'github-token' (Secret text = GitHub PAT with repo:status scope).
// If credential is missing the build still passes - status posting is skipped silently.
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
                curl -s -o /dev/null -w "GitHub status API response: %{http_code}\\n" \\
                  -H "Authorization: token ${GH_TOKEN}" \\
                  -H "Content-Type: application/json" \\
                  -X POST \\
                  -d '${payload}' \\
                  "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/statuses/${commitHash}"
            """
        }
    } catch (Exception e) {
        echo "GitHub status update skipped (add github-token credential to enable): ${e.message}"
    }
}
