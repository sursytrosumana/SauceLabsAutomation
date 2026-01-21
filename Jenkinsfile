pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/sursytrosumana/SauceLabsAutomation.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest -q'
            }
        }
    }
}
