pipeline {
    agent any
    parameters {
        string(name: 'BRANCH_NAME', description: 'Name of the branch to build')
    }
    environment {
        SERVICE_NAME = "counter-service"
        DOCKER_REGISTRY = "tfrisz"
        DOCKERFILE_PATH = "app"
        DOCKER_REGISTRY_CREDENTIALS = 'dockerhub_creds'
        REPO_URL = "https://github.com/tom1187/counter-service.git"
        ref="refs/heads/feature/test1"
    }
    stages {
        stage('Process Webhook') {
            when {
                expression {env?.ref != null}
            }
            steps {
                script {
                    echo "Received webhook for branch: ${env.ref}"
                    def branchName = "${env.ref}".replace('refs/heads/', '')
                    env.BRANCH_NAME = branchName
                    env.BRANCH = branchName.replace("/","_")
                    env.DOCKER_IMAGE_TAG = "${BRANCH}-${env.BUILD_NUMBER}"
                    echo "Using branch: ${branchName}."
                    echo "env.BRANCH_NAM: ${env.BRANCH_NAM}"
                }
            }
        }
        stage('Process Manual Exec') {
            when {
                expression {"${params.BRANCH_NAME}" != ""}
            }
            steps {
                script {
                    echo "Received manual execution for branch: ${params.BRANCH_NAME}"
                    env.BRANCH_NAME = "${params.BRANCH_NAME}"
                    env.BRANCH = "${params.BRANCH_NAME}".replace("/","_")
                    env.DOCKER_IMAGE_TAG = "${env.BRANCH}-${env.BUILD_NUMBER}"
                    echo "Using branch: ${env.BRANCH_NAME}."
                }
            }
        }
        stage('Checkout') {
            steps {
                echo "Checking out code from ${REPO_URL} on branch ${env.BRANCH_NAME}"
                checkout([$class: 'GitSCM', branches: [[name: "${env.BRANCH_NAME}"]], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: "${REPO_URL}"]]])
            }
        }
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image for ${SERVICE_NAME}:${DOCKER_IMAGE_TAG}"
                dir("${DOCKERFILE_PATH}"){
                    sh "docker build -t ${DOCKER_REGISTRY}/${SERVICE_NAME}:${DOCKER_IMAGE_TAG} -f Dockerfile ."
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                echo "Pushing Docker image ${SERVICE_NAME}:${DOCKER_IMAGE_TAG} to ${DOCKER_REGISTRY}"
                dir("${DOCKERFILE_PATH}"){
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDENTIALS}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        sh "docker push ${DOCKER_REGISTRY}/${SERVICE_NAME}:${DOCKER_IMAGE_TAG}"
                    }
                }
            }
        }
        stage('Deploy to Target Environment') {
            steps {
                echo "Deploying ${SERVICE_NAME}:${DOCKER_IMAGE_TAG} to target environment"
                sh """cat > docker_compose_env <<EOF
                      REDIS_CONTAINER_NAME=redis_${DOCKER_IMAGE_TAG}
                      COUNTER_SERVICE_CONTAINER_NAME=${SERVICE_NAME}_${DOCKER_IMAGE_TAG}
                      COUNTER_SERVICE_IMAGE=${DOCKER_REGISTRY}/${SERVICE_NAME}:${DOCKER_IMAGE_TAG}
                      EOF
                """

                sh 'docker-compose up -d --env-file docker_compose_env'
            }
        }
    }
}
