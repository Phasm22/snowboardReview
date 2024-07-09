pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    docker.image('python:3.9').inside {
                        sh '''
                            mkdir -p /tmp/pip-cache
                            pip install --upgrade pip --cache-dir /tmp/pip-cache
                            pip install -r requirements.txt --cache-dir /tmp/pip-cache
                        '''
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image('python:3.9').inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-django-app .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 8050:8050 my-django-app'
            }
        }
    }
}
