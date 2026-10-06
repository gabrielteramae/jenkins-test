pipeline {
    agent any

    environment {
        IMAGE_NAME = "task-api"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Instalar dependências') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Rodar testes') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --junitxml=resultado-testes.xml
                '''
            }
            post {
                always {
                    junit 'resultado-testes.xml'
                }
            }
        }

        stage('Build da imagem Docker') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Smoke test do container') {
            steps {
                sh '''
                    NAME="task-api-smoke-${BUILD_NUMBER}"
                    docker rm -f "$NAME" >/dev/null 2>&1 || true
                    docker run -d --name "$NAME" -p 8001:8000 "${IMAGE_NAME}:${IMAGE_TAG}"
                    ok=0
                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        if curl --fail --silent http://localhost:8001/health; then
                            ok=1
                            break
                        fi
                        sleep 1
                    done
                    test "$ok" = 1
                '''
            }
            post {
                always {
                    sh '''
                        NAME="task-api-smoke-${BUILD_NUMBER}"
                        docker stop "$NAME" || true
                        docker rm "$NAME" || true
                    '''
                }
            }
        }

        stage('Deploy (simulado)') {
            when {
                branch 'main'
            }
            steps {
                echo "Deploy da imagem ${IMAGE_NAME}:${IMAGE_TAG} para produção (etapa simulada)."
                // Aqui entraria, por exemplo:
                // sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} seu-registry/${IMAGE_NAME}:${IMAGE_TAG}"
                // sh "docker push seu-registry/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo "Pipeline concluído com sucesso — build #${env.BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline falhou — verifique os logs do estágio que quebrou"
        }
        always {
            sh 'docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true'
        }
    }
}
