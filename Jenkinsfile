pipeline {
    agent any

    parameters {
        string(name: 'CUTOFF', defaultValue: '100', description: 'Ilość wierszy do odcięcia')
	    string(name: 'KAGGLE_USERNAME', defaultValue: '', description: 'Kaggle username')
        password(name: 'KAGGLE_KEY', defaultValue: '', description: 'Kaggle API key')
    }

    stages {
        stage('Clone repo') {
            steps {
                git branch: "main", url: "https://git.wmi.amu.edu.pl/s464937/ium_464937"
            }
        }

        stage('Download and preprocess') {
            environment {
                    KAGGLE_USERNAME = "szymonbartanowicz"
                    KAGGLE_KEY = "4692239eb65f20ec79f9a59ef30e67eb"
                }
            steps {
                withEnv([
                    "KAGGLE_USERNAME=${env.KAGGLE_USERNAME}",
                    "KAGGLE_KEY=${env.KAGGLE_KEY}"
                ]) {
                    sh "bash ./script1.sh ${params.CUTOFF}"
                }
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'data/*', onlyIfSuccessful: true
            }
        }
    }
}