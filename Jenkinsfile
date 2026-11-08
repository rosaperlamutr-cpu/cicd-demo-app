pipeline {
    agent any

    parameters {
        string(name: 'REPO_URL', defaultValue: 'https://github.com/ThisIsMikeyS/cicd-demo-app', description: 'HTTPS-ссылка на ваш Fork репозитория')
        string(name: 'GIT_BRANCH', defaultValue: 'master', description: 'Ветка для сборки')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Выполнять unit-тесты')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "*/${params.GIT_BRANCH}"]], 
                        userRemoteConfigs: [[url: params.REPO_URL]]
                    ])
                    
                    def gitBranch = sh(script: "git rev-parse --abbrev-ref HEAD", returnStdout: true).trim()
                    def gitCommit = sh(script: "git rev-parse HEAD", returnStdout: true).trim()
                    
                    echo "Ветка: ${gitBranch}"
                    echo "SHA коммита: ${gitCommit}"
                    env.GIT_COMMIT_SHA = gitCommit
                }
            }
        }

        stage('Validate') {
            steps {
                script {
                    def requiredFiles = ['README.md', 'requirements.txt', 'src', 'tests']
                    def missing = []
                    
                    for (file in requiredFiles) {
                        if (!fileExists(file)) {
                            missing.add(file)
                        }
                    }
                    
                    if (!missing.isEmpty()) {
                        error "Отсутствуют обязательные элементы: ${missing.join(', ')}"
                    }
                }
            }
        }

        stage('Test') {
            when {
                expression { return params.RUN_TESTS }
            }
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m unittest discover -s tests -v'
                    } else {
                        bat 'python -m unittest discover -s tests -v'
                    }
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    def buildInfo = "Номер сборки Jenkins: ${env.BUILD_NUMBER}\nSHA коммита: ${env.GIT_COMMIT_SHA}"
                    writeFile file: 'build-info.txt', text: buildInfo
                    
                    if (isUnix()) {
                        sh 'tar -czf app.tar.gz --exclude=app.tar.gz --exclude=.git .'
                    } else {
                        bat 'tar -czf app.tar.gz --exclude=app.tar.gz --exclude=.git .'
                    }
                }
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'app.tar.gz', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Сборка успешно завершена.'
        }
        failure {
            echo 'Сборка завершилась с ошибкой.'
        }
        always {
            echo "Статус сборки: ${currentBuild.currentResult}"
        }
    }
}
