pipeline {
    agent any

    environment {
        PROJECT_ID  = "k8s-learning-499223"
        CLUSTER     = "flask-cluster"
        ZONE        = "us-central1-a"
        IMAGE       = "gcr.io/k8s-learning-499223/flask-app"
        VERSION     = "4.0.${BUILD_NUMBER}"
        NAMESPACE   = "flask-prod"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code for version ${VERSION}..."
            }
        }

        stage('Build & Push Image') {
            steps {
                echo "Building AMD64 Docker image ${IMAGE}:${VERSION}..."
                sh """
                    docker buildx build \
                        --platform linux/amd64 \
                        -t ${IMAGE}:${VERSION} \
                        -t ${IMAGE}:latest \
                        --push .
                """
                echo "Image pushed: ${IMAGE}:${VERSION}"
            }
        }

        stage('Update ConfigMap') {
            steps {
                echo "Updating ConfigMap with new version..."
                sh """
                    kubectl create configmap flask-config \
                        --from-literal=APP_VERSION=${VERSION} \
                        --from-literal=APP_ENV=production \
                        --from-literal=LOG_LEVEL=info \
                        --namespace=${NAMESPACE} \
                        --dry-run=client -o yaml | kubectl apply -f -
                """
            }
        }

        stage('Deploy to GKE') {
            steps {
                echo "Deploying ${IMAGE}:${VERSION} to GKE..."
                sh """
                    kubectl set image deployment/flask-deployment \
                        flask=${IMAGE}:${VERSION} \
                        --namespace=${NAMESPACE}
                """
                sh """
                    kubectl rollout status deployment/flask-deployment \
                        --namespace=${NAMESPACE} \
                        --timeout=120s
                """
                echo "Deployment complete!"
            }
        }

        stage('Verify') {
            steps {
                echo "Verifying deployment..."
                sh """
                    kubectl get pods -n ${NAMESPACE}
                """
                sh """
                    kubectl get service flask-service -n ${NAMESPACE}
                """
                echo "Version ${VERSION} is live!"
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS! Version ${VERSION} deployed to GKE."
        }
        failure {
            echo "Pipeline FAILED — rolling back..."
            sh "kubectl rollout undo deployment/flask-deployment -n ${NAMESPACE} || true"
            echo "Rollback complete."
        }
        always {
            echo "Pipeline finished."
        }
    }
}
