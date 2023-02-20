pipeline {
    agent any
    parameters {
        string(name: 'BRANCH_NAME', description: 'Name of the branch to build')
    }
    environment {
        SERVICE_NAME = "counter-service"
        BRANCH = "${env.BRANCH_NAME}".replace("/","_")
        DOCKER_IMAGE_TAG = "${BRANCH}-${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = "tfrisz"
        DOCKERFILE_PATH = "app"
        DOCKER_REGISTRY_CREDENTIALS = 'dockerhub_creds'
        REPO_URL = "https://github.com/tom1187/counter-service.git"
    }
    stages {
        stage('Process Webhook') {
            when {
                expression { "${params.BRANCH_NAME}" == '' }
            }
            steps {
                script {
                    def payload = readJSON text: env.payload
                    def branchName = payload.head_commit.ref.replace('refs/heads/', '')
                    params.BRANCH_NAME = branchName
                    env.BRANCH = branchName.replace("/","_")
                    echo "Received webhook for branch: $branchName"
                }
            }
        }
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: "${params.BRANCH_NAME}"]], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: "${REPO_URL}"]]])
            }
        }
        stage('Build Docker Image') {
            steps {
                dir("${DOCKERFILE_PATH}"){
                    sh "docker build -t ${DOCKER_REGISTRY}/${SERVICE_NAME}:${DOCKER_IMAGE_TAG} -f Dockerfile ."
                }
            }
        }
        stage('Push Docker Image') {
            steps {
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
                dir("${DOCKERFILE_PATH}"){
                    sh "docker pull ${DOCKER_REGISTRY}/${SERVICE_NAME}:${DOCKER_IMAGE_TAG}"
                    sh "sed -i 's|\\'placeholder_image'|${DOCKER_REGISTRY}/${SERVICE_NAME}:${DOCKER_IMAGE_TAG}|g' docker-compose.yaml"
                    sh "cat docker-compose.yaml"
                    sh 'docker-compose up -d'
                }
            }
        }
    }
}


