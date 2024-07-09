pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    docker.image('python:3.9').inside('-u root') {
                        sh '''
                            python -m venv testenv
                            chmod -R a+rwx testenv/lib/python3.9/site-packages
                            chmod -R a+rwx testenv/bin
                            . testenv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image('python:3.9').inside('-u root') {
                        sh '''
                            . testenv/bin/activate
                            python manage.py test
                        '''
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
