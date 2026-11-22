pipeline {
    agent any

    parameters {
        string(name: 'REPO_URL', defaultValue: 'https://github.com/rosaperlamutr-cpu/cicd-demo-app.git', description: 'URL вашего форка')
        string(name: 'GIT_BRANCH', defaultValue: 'master', description: 'Ветка для сборки')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Запускать тесты и линтер')
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Развернуть локально')
        string(name: 'APP_PORT', defaultValue: '18080', description: 'Порт хоста (1024-65535)')
    }

    environment {
        SHORT_SHA = "${env.GIT_COMMIT?.take(7) ?: 'unknown'}"
        IMAGE_TAG = "student-app:${env.BUILD_NUMBER}-${env.SHORT_SHA}"
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    if (!params.REPO_URL?.trim()) error "REPO_URL cannot be empty."
                    if (!params.GIT_BRANCH?.trim()) error "GIT_BRANCH cannot be empty."
                    def port = params.APP_PORT as Integer
                    if (port < 1024 || port > 65535) error "APP_PORT must be 1024-65535."
                }
                git url: params.REPO_URL, branch: params.GIT_BRANCH
                echo "Checked out ${env.GIT_COMMIT} (Build #${env.BUILD_NUMBER})"
            }
        }

        stage('Validate') {
            steps {
                script {
                    def requiredFiles = ['Dockerfile', 'Jenkinsfile', 'ansible/deploy.yml', 'app.py']
                    def missingFiles = requiredFiles.findAll { !fileExists(it) }
                    if (!missingFiles.isEmpty()) error "Missing files: ${missingFiles.join(', ')}"
                    if (params.DEPLOY && !params.RUN_TESTS) error "DEPLOY=true запрещен при RUN_TESTS=false!"
                }
            }
        }

        stage('Lint') {
            when { expression { params.RUN_TESTS } }
            steps {
                sh 'python3 -m pip install flake8 --break-system-packages'
                sh 'python3 -m flake8 src tests app.py'
            }
        }

        stage('Test') {
            when { expression { params.RUN_TESTS } }
            steps {
                sh 'python3 -m pip install coverage --break-system-packages'
                sh 'python3 -m coverage run -m unittest discover -s tests'
                sh 'python3 -m coverage xml -o coverage.xml'
            }
            post {
                always { archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    sh "docker build -t ${env.IMAGE_TAG} ."
                    def buildInfo = "SHA: ${env.GIT_COMMIT}\nBranch: ${params.GIT_BRANCH}\nBuild: ${env.BUILD_NUMBER}\nImage: ${env.IMAGE_TAG}"
                    writeFile file: 'build-info.txt', text: buildInfo
                    archiveArtifacts artifacts: 'build-info.txt'
                }
            }
        }

        stage('Deploy') {
            when { expression { params.DEPLOY } }
            steps {
                sh """
                    ansible-playbook ansible/deploy.yml \
                    -e "build_number=${env.BUILD_NUMBER}" \
                    -e "short_sha=${env.SHORT_SHA}" \
                    -e "host_port=${params.APP_PORT}"
                """
            }
        }

        stage('Verify') {
            when { expression { params.DEPLOY } }
            steps {
                sh "curl --fail http://127.0.0.1:${params.APP_PORT}/health"
            }
        }
    }

    post {
        always { echo "Pipeline finished: ${currentBuild.currentResult}" }
    }
}
