pipeline {
    agent {
        node {
            label 'worker-node'
            }
      }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                docker build -t ${JOB_NAME}:${BUILD_ID} .
                '''
            }
        }
        stage('Unit Test') {
            steps {
                echo "Testing.."
                script {
                    docker.image("${JOB_NAME}:${BUILD_ID}").inside("--user 0 "){
                        sh """
                        pylint --msg-template='{path}:{line}: [{msg_id}, {obj}] {msg} ({symbol})' --output  pylint.log  ProfileWeb   || true
                        """
                        recordIssues(
                            tool: pyLint(pattern: 'pylint.log'),
                            )
                    }
                    docker.image("${JOB_NAME}:${BUILD_ID}").inside(""){
                        sh """
                        coverage  run  -m unittest Tests/ProfileWeb/*.py
                        coverage xml
                        """
                        recordCoverage(tools: [[parser: 'COBERTURA', pattern: "coverage.xml"]],
                            id: 'Cobertura', name: 'python Coverage',
                            sourceCodeRetention: 'EVERY_BUILD',
                            )
                    }
                }
            }
        }
        stage('Selenium Test') {
            steps {
                script {
                    sh "docker rm mongodb serverundertest test-chrome || true"
                    docker.image("mongo").withRun("-h mongodb --name mongodb"){ mongo ->
                        sleep 2
                        docker.image("${JOB_NAME}:${BUILD_ID}").withRun("--name serverundertest -h serverundertest --link mongodb"){ app ->
                            sleep 10
                            docker.image("selenium/standalone-chrome:112.0").withRun("-p 4444:4444 --name test-chrome -h test-chrome --link serverundertest -e 'SE_NODE_OVERRIDE_MAX_SESSIONS=true' -e 'SE_NODE_MAX_SESSIONS=1' "){ chrome ->
                                sleep 5
                                docker.image("${JOB_NAME}:${BUILD_ID}").inside("--link test-chrome --link mongodb ") {
                                   try {
                                    sh "python -m unittest -v  Tests/End-to-end-tests/*.py"
                                   }catch (Exception e) {
                                     // sleep  3600
                                    echo "Tests failed: ${e.message}"
                                    currentBuild.result = 'FAILURE'
                                    error("Tests failed: ${e.message}")
                                   }
                                }
                            }
                        }

                    }
                }
            }
        }
        stage('Upload') {
            steps {
                sh '''
                docker tag ${JOB_NAME}:${BUILD_ID}  registry-vpc.us-west-1.aliyuncs.com/gwubc/${JOB_NAME}:${BUILD_ID}
                docker push registry-vpc.us-west-1.aliyuncs.com/gwubc/${JOB_NAME}:${BUILD_ID}
                '''
            }
        }
        stage('local deploy') {
            steps {
                echo 'Deliver....'
                sh '''
                docker compose stop
                docker compose create
                docker compose start
                '''
            }
        }
    }
}
