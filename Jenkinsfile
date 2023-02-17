pipeline {
    agent any
    parameters {
        string(name: 'BRANCH_NAME', description: 'Name of the branch to build', defaultValue: 'main')
    }
    environment {
        SERVICE_NAME = 'counter-service'
        IMAGE_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
        KUBE_NAMESPACE = 'default'
        REPO_URL = 'https://github.com/tom1187/counter-service.git'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: "${params.BRANCH_NAME}"]], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: ${REPO_URL}]]])
            }
        }
        stage('Build image') {
            steps {
                sh "docker build -t tfirsz/${SERVICE_NAME}:${IMAGE_TAG} ."
                sh "docker push tfirsz/${SERVICE_NAME}:${IMAGE_TAG}"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl config use-context my-kubernetes-cluster"
                sh "kubectl set image deployment/${SERVICE_NAME} ${SERVICE_NAME}=tfrisz/${SERVICE_NAME}:${IMAGE_TAG} -n ${KUBE_NAMESPACE}"
                sh "kubectl rollout status deployment/${SERVICE_NAME} -n ${KUBE_NAMESPACE}"
            }
        }
    }
}
