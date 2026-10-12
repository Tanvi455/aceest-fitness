pipeline {
    agent any

    stages {
        stage('Build and Test') {
            steps {
                sh 'docker build --target test -t aceest-fitness:test .'
            }
        }

        stage('Build Runtime Image') {
            steps {
                sh 'docker build -t aceest-fitness:jenkins .'
            }
        }
    }
}