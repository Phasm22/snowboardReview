pipeline {
    agent any

    stages {
        stage('Install Python and Pip') {
            steps {
                sh '''
                apt-get update
                apt-get install -y python3 python3-pip
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python3 manage.py test'
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
