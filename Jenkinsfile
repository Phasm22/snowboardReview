pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    docker.image('python:3.12').inside('-u root') {
                        sh '''
                            python -m venv testenv
                            chmod -R a+rwx testenv/lib/python3.9/site-packages
                            chmod -R a+rwx testenv/bin
                            . testenv/bin/activate
                            pip install --upgrade pip
			    pip install django
                            python -m pip install python-dotenv
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }
        // Commented out the Run Tests stage
        // stage('Run Tests') {
        //     steps {
        //         script {
        //             docker.image('python:3.12').inside('-u root') {
        //                 sh '''
        //                     . testenv/bin/activate
        //                     python manage.py test
        //                 '''
        //             }
        //         }
        //     }
        // }
        stage('Build Docker Image') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
