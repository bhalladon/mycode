artifact_workspace = 'none'

// function for sending the notification
def sendNotification(status, color, description) {
    def jobName = env.JOB_NAME.replaceAll('%2F', '/').tokenize('/')[0]
    def branchName = env.JOB_NAME.replaceAll('%2F', '/').tokenize('/')[1]
    def buildNumber = env.BUILD_NUMBER
    def allureReportUrl = "http://zaml-saas-dev-jenkins.clients.zaml.zestfinance.com/job/${jobName}/job/${branchName}/${buildNumber}/allure/"
    def message = "Branch Name: ${branchName}\n${status}: Allure Report: ${allureReportUrl} ${status == 'Success' ? ':thumbsup:' : ':thumbsdown:'}\nBuild triggered by: ${TRIGGERED_BY}"

    // GitHub status update
    sh """
        curl -L -u ${env.GITHUB_API_TOKEN} ${env.GITHUB_STATUS_URL} \
        -H "Content-Type: application/json" \
        -H "Accept: application/vnd.github.v3+json" \
        -X POST \
        -d '{"state": "${status.toLowerCase()}", "description": "Building the environment and testing", "context": "HollaBot", "target_url": "${env.BUILD_URL}"}'
   """

    slackSend baseUrl: 'https://hooks.slack.com/services/',
              channel: 'iss-test-automation-cicd-alerts',
              color: color,
              message: message,
              tokenCredentialId: 'iss-test-automation-cicd-alerts-slack',
              username: 'pradeep'
}

def get_aws_access_keys() {
    // First check PR_DOCKER_IMAGE and set ENV if needed
    if (env.PR_DOCKER_IMAGE?.trim()) {
        test_env = 'dev'
        echo "Setting environment to: ${test_env} due to PR_DOCKER_IMAGE being set"
    } else {
        test_env = env.ENV
    }
    // Mapping environments to Jenkins credential IDs
    def envCredentialsMap = [
        'sandbox': 'TA_STAGE_MH_AWS_CREDENTIALS',
        'dev'    : 'TA_DEV_MH_AWS_CREDENTIALS',
        'prod'   : 'test-automation-eng-user'
    ]
    // Retrieve the correct credentials ID for the selected environment
    def credentialsId = envCredentialsMap[test_env]

    if (credentialsId) {
        def awsCredentials = [:]  // Initialize a map to store AWS credentials

        // Use withCredentials with a code block to assign credentials to env variables
        withCredentials([
            [$class: 'AmazonWebServicesCredentialsBinding',
             credentialsId: credentialsId,
             accessKeyVariable: 'AWS_ACCESS_KEY_ID',
             secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']
        ]) {
            awsCredentials['AWS_ACCESS_KEY_ID'] = env.AWS_ACCESS_KEY_ID
            awsCredentials['AWS_SECRET_ACCESS_KEY'] = env.AWS_SECRET_ACCESS_KEY
        }

        return awsCredentials
    } else {
        error "No valid credentials ID found for environment: ${env.ENV}"
    }
}

def get_legacy_aws_access_keys() {
    def awsCredentials = [:]  // Initialize a map to store AWS credentials

    // Use withCredentials with a code block to assign credentials to env variables
    withCredentials([
        [$class: 'AmazonWebServicesCredentialsBinding',
         credentialsId: 'TA_LEGACY_AWS_CREDENTIALS',
         accessKeyVariable: 'LEGACY_AWS_ACCESS_KEY_ID',
         secretKeyVariable: 'LEGACY_AWS_SECRET_ACCESS_KEY']
    ]) {
        awsCredentials['LEGACY_AWS_ACCESS_KEY_ID'] = env.LEGACY_AWS_ACCESS_KEY_ID
        awsCredentials['LEGACY_AWS_SECRET_ACCESS_KEY'] = env.LEGACY_AWS_SECRET_ACCESS_KEY
    }

    return awsCredentials
}

def set_s3_archive_flag() {
    // Function to set the boolean value to the 'ENABLE_SCORE_ARCHIVE',
    // based on the environment selected
    if (env.ENV == 'prod') {
        // As discussed we are not hard coding ENABLE_SCORE_ARCHIVE to False for prod env
        // We are not removing code, to use in future (if required)
        // value = false
        value = env.S3_ARCHIVE_FLAG
    } else {
        value = env.S3_ARCHIVE_FLAG
    }
    return value
}

def get_build_triggered_by() {
    def triggered_by

    // Check Build Cause
    try {
        // Using currentBuild and env variables for better reliability
        if (env.BUILD_USER != null) {
            triggered_by = env.BUILD_USER
            echo "Triggered by user: ${triggered_by}"
        }
        else if (env.BUILD_UPSTREAM_URL != null) {
            "${currentBuild.getBuildCauses()[0].upstreamUrl?:''}"
            triggered_by = "Upstream job: ${currentBuild.getBuildCauses()[0].upstreamUrl?:''}, Build number: ${currentBuild.getBuildCauses()[0].upstreamBuild?:''}"
            echo "Triggered by upstream: ${triggered_by}"
        }
        else {
            triggered_by = "Cron Job"
            echo "Triggered by cron job"
        }
    } catch (Exception e) {
        echo "Error determining build trigger: ${e.getMessage()}"
        triggered_by = "Unknown"
    }

    echo "TRIGGERED_BY is: ${triggered_by}"
    return triggered_by
}

// Multi-branch pipeline. Build on Monday at 9.30 PM PST and Friday once a day at 9.30 PM PST
// Explanation: 30 5 * * 1,5
// 30 → Minute (30th minute of the hour)
// 5 → Hour (5 AM UTC, which is 9:30 PM PST)
// * → Day of the month (every day)
// * → Month (every month)
// 1,5 → Days of the week (Monday = 1, Friday = 5)
CRON_SETTINGS = BRANCH_NAME == "main" ? '''30 5 * * 1,5 % TEST_ENVIRONMENT=sandbox;CLIENT_CONFIG_ENV=sandbox;TESTS_DIR=src/tests;CODE_VERSION=v2;CREATE_POSTMAN_COLLECTION=false;REQUEST_SAMPLING=true;REQUEST_SAMPLING_COUNT=5;TEST_RERUN=0;CLIENT_SAMPLING=false;ENABLE_SCORE_ARCHIVE=false;''' : ""

pipeline {
    agent {
        docker {
            image '777724356028.dkr.ecr.us-east-1.amazonaws.com/zest-backend-api-automation-base:v2'
           args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    triggers {
        parameterizedCron(CRON_SETTINGS)
    }
    parameters {
        string defaultValue: '', description: 'Optional: enter release build number/date', name: 'RELEASE', trim: true
        choice choices: ['v2', 'v1'], description: 'Required: select code version \n v1: Starts from MH terraform github repo \n v2: Starts from client config', name: 'CODE_VERSION'
        string defaultValue: '0', description: 'Optional: enter value for test re-run in case of failure', name: 'TEST_RERUN', trim: true
        string defaultValue: '', description: 'Optional: specify the Docker image path to run the build against a feature branch', name: 'PR_DOCKER_IMAGE', trim: true
        choice choices: ['sandbox', 'dev', 'prod'], description: 'Required: select test environment \n Note: If PR_DOCKER_IMAGE is set, environment will default to dev', name: 'TEST_ENVIRONMENT'
        choice choices: ['sandbox', 'prod'], description: 'Required: select the environment to obtain valid client configuration', name: 'CLIENT_CONFIG_ENV'
        string defaultValue: 'src/tests', description: 'Required: directory for automated tests \n Do not change this settings', name: 'TESTS_DIR', trim: true
        booleanParam defaultValue: false, description: 'Optional: create Postman Collection Flag', name: 'CREATE_POSTMAN_COLLECTION'
        booleanParam defaultValue: false, description: 'Optional: override Postman Collection Flag', name: 'OVERRIDE_POSTMAN_COLLECTION'
        booleanParam defaultValue: true, description: 'Optional: execute the test with a limited number of requests, \n provide the request sampling count as a integer value in REQUEST_SAMPLING_COUNT', name: 'REQUEST_SAMPLING'
        string defaultValue: '5', description: 'Optional: provide the request sampling count as integer value', name: 'REQUEST_SAMPLING_COUNT', trim: true
        booleanParam defaultValue: false, description: 'Optional: to run tests for specific clients \n For v1 - Please provide the client file name(s) in CLIENT_SAMPLING_FILENAMES \n For v2- Please provide the client id(s) in CLIENT_SAMPLING_CLIENT_IDS', name: 'CLIENT_SAMPLING'
        string defaultValue: '', description: 'Optional: For v1, provide comma-separated client environment file names \n Also, check the CLIENT_SAMPLING checkbox to run tests for these specific clients', name: 'V1_CLIENT_SAMPLING_FILENAMES', trim: true
        string defaultValue: '', description: 'Optional: For v2, provide comma-separated client IDs. \n Also, check the CLIENT_SAMPLING checkbox to run tests for these specific clients', name: 'V2_CLIENT_SAMPLING_CLIENT_IDS', trim: true
        booleanParam defaultValue: false, description: 'Optional: Select this option to generate score archives. When ENABLE_SCORE_ARCHIVE is selected, the "X-Zest-Disable-Score-Archive" header will be set to "False".', name: 'ENABLE_SCORE_ARCHIVE'
        string defaultValue: '', description: 'Optional:\n Enter any additional query parameter for v6 scoring API endpoint.\n By default endpoint is: "/api/v6/scoring".\n If any additional parameter is required, consider the following example.\n Example for a single query parameter -> return-model-scoring-requests=true\n if you want to add multiple query parameters then conside the following example.\n Example for multiple query parameters -> return-model-scoring-requests=true&return-bureau-requests=false', name: 'V6_SCORING_API_QUERY_PARAMETER'
        string defaultValue: 'zest-backed-api-automation', description: 'Repository name', name: 'REPONAME', trim: true
        string defaultValue: '', description: 'GIT_COMMIT id', name: 'GIT_COMMIT', trim: true
    }

    environment {
        REPONAME = "${params.REPONAME}"
        GITHUB_API_TOKEN = credentials('iss-automation-github-status-token')
        GIT_COMMIT = "${params.GIT_COMMIT ?: env.GIT_COMMIT}"
        BUILD_URL = "http://zaml-saas-dev-jenkins.clients.zaml.zestfinance.com/job/${JOB_NAME.split('/')[0]}/job/${JOB_NAME.split('/')[1]}/${BUILD_NUMBER}"
        GITHUB_STATUS_URL = "https://api.github.com/repos/Katlean/$REPONAME/statuses/${env.GIT_COMMIT}?access_token=$GITHUB_API_TOKEN"
        ARTIFACTORY_CREDS = credentials('build-push-user-artifactory')
        ARTIFACTORY_PATH = 'zaml.jfrog.io/zaml/api/pypi/zest_pypi'
        ARTIFACTORY_URL = "https://$ARTIFACTORY_PATH"
        PIP_INDEX_URL = "https://$ARTIFACTORY_CREDS_USR:$ARTIFACTORY_CREDS_PSW@$ARTIFACTORY_PATH/simple"
        TESTS_DIR = "src/tests"
        RELEASE = "${params.RELEASE}"
        MAX_RUNS = "${params.TEST_RERUN}"
        WORKERS = 6 // Increasing the number of workers will result in login failure due to high load.
        MAX_FAIL = 20
        PR_DOCKER_IMAGE = "${params.PR_DOCKER_IMAGE}"
        ECR_URL = '777724356028.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = 'backend-interactive-scoring-service'
        AWS_DEFAULT_REGION = 'us-east-1'
        PORT = 3000
        ENV_FILE_PATH = 'utils/iss_pr_env.env'
        CONTAINER_NAME = "iss-${env.ENV}-container-${env.BUILD_NUMBER}"
        NETWORK_NAME = "iss_${env.ENV}_network_${env.BUILD_NUMBER}" // Custom network with build number
        DOCKER_IMAGE = "${env.ECR_URL}/${env.ECR_REPOSITORY}:${env.PR_DOCKER_IMAGE}"
        PATH = "$PATH:/usr/src/app/.local/bin"
        ENV = "${params.TEST_ENVIRONMENT}"
        CLIENT_CONFIG_ENV = "${params.CLIENT_CONFIG_ENV}"
        BUILD_USER = "${currentBuild.getBuildCauses()[0].userId?:''}"
        BUILD_UPSTREAM_URL = "${currentBuild.getBuildCauses()[0].upstreamUrl?:''}"
        BUILD_CAUSE = "${currentBuild.getBuildCauses()}"
        TRIGGERED_BY = "${env.BUILD_USER?:env.BUILD_UPSTREAM_URL?:'CRON Job'}"
        // Feature Flags
        CREATE_POSTMAN_COLLECTION_FLAG = "${params.CREATE_POSTMAN_COLLECTION}"
        OVERRIDE_POSTMAN_COLLECTION_FLAG = "${params.OVERRIDE_POSTMAN_COLLECTION}"
        REQUEST_SAMPLING_FLAG = "${params.REQUEST_SAMPLING}"
        REQUEST_SAMPLING_COUNT = "${params.REQUEST_SAMPLING_COUNT}"
        CODE_VERSION = "${params.CODE_VERSION}"
        CLIENT_SAMPLING_FLAG = "${params.CLIENT_SAMPLING}"
        CLIENT_SAMPLING_FILENAMES = "${params.V1_CLIENT_SAMPLING_FILENAMES}"
        CLIENT_SAMPLING_CLIENT_IDS = "${params.V2_CLIENT_SAMPLING_CLIENT_IDS}"
        S3_ARCHIVE_FLAG = "${params.ENABLE_SCORE_ARCHIVE}"
        // sh command
        SHCOMMAND = "pytest -v -s ${TESTS_DIR} --env ${ENV} --client_config_env ${CLIENT_CONFIG_ENV} --code_version ${CODE_VERSION} --reruns ${MAX_RUNS} -p no:cacheprovider --create_postman_collection ${CREATE_POSTMAN_COLLECTION_FLAG} --override_postman_collection ${OVERRIDE_POSTMAN_COLLECTION_FLAG} --junitxml=pytest-report.xml --html=pytest-report.html  --alluredir=./allure-results"
        POSTMAN_API_KEY = credentials('POSTMAN_API_KEY_FOR_ISS_SCORING_AUTOMATION')
    }
    stages {
       stage('Pending') {
            steps {
                sh '''
                    curl -L -u "$GITHUB_API_TOKEN" "$GITHUB_STATUS_URL" \
                    -H "Content-Type: application/json" \
                    -H "Accept: application/vnd.github.v3+json" \
                    -X POST \
                    -d '{"state": "pending", "description": "Building the environment and testing", "context": "HollaBot", "target_url": "'$BUILD_URL'"}'
                '''
            }
        }
        stage('Set AWS Credentials & ENABLE_SCORE_ARCHIVE Flag status') {
                  steps {
                      script {
                          echo "Build triggered using function is: ${get_build_triggered_by()}"
                          env.TRIGGERED_BY = env.BUILD_USER ?: env.BUILD_UPSTREAM_URL ?: 'CRON Job'
                          echo "Build cause: ${env.BUILD_CAUSE}"
                          echo "Build triggered by: ${env.TRIGGERED_BY}"
                          def awsKeys = get_aws_access_keys()
                          if (awsKeys) {
                              env.AWS_ACCESS_KEY_ID = awsKeys['AWS_ACCESS_KEY_ID']
                              env.AWS_SECRET_ACCESS_KEY = awsKeys['AWS_SECRET_ACCESS_KEY']
                          }
                          def legacyKeys = get_legacy_aws_access_keys()
                          if (legacyKeys) {
                              env.LEGACY_AWS_ACCESS_KEY_ID = legacyKeys['LEGACY_AWS_ACCESS_KEY_ID']
                              env.LEGACY_AWS_SECRET_ACCESS_KEY = legacyKeys['LEGACY_AWS_SECRET_ACCESS_KEY']
                          }
                          def s3_archive_value = set_s3_archive_flag()
                          if (s3_archive_value) {
                              env.ENABLE_SCORE_ARCHIVE = s3_archive_value
                          }
                      }
                  }
        }
        stage('Clean Up Docker Containers') {
            steps {
                script {
                    echo "Stopping and removing containers using port ${PORT}"

                    // Stop containers that might be using the port
                    sh "docker ps -q --filter 'publish=${PORT}' | xargs -r docker stop"
                    sh "docker ps -aq --filter 'publish=${PORT}' | xargs -r docker rm"

                    // Prune all stopped containers to free up space
                    sh "docker container prune -f"

                    // Remove dangling (unused) images
                    sh "docker images -q --filter 'dangling=true' | xargs -r docker rmi"
              }
           }
        }
        stage('Create Network & Pull Docker Image') {
            steps {
                script {
                    // Check if PR_DOCKER_IMAGE is not empty or null
                    if (env.PR_DOCKER_IMAGE?.trim()) {
                        // Create a custom Docker network
                        echo "Creating a custom Docker network"
                        sh "docker network create --attachable ${NETWORK_NAME}"

                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                        credentialsId: 'ecr',
                                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                            // Authenticate with AWS ECR
                            sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${ECR_URL}"

                            // Pull the Docker image
                            sh "docker pull ${ECR_URL}/${ECR_REPOSITORY}:${PR_DOCKER_IMAGE}"

                            // Run the pulled Docker container
                            echo "Running the pulled Docker container"
                            sh "docker run -d --name ${CONTAINER_NAME} --env-file ${ENV_FILE_PATH} -p ${PORT} ${ECR_URL}/${ECR_REPOSITORY}:${PR_DOCKER_IMAGE}"

                            // Retrieve the dynamically allocated host port
                            def hostPort = sh(script: "docker port ${CONTAINER_NAME} ${PORT} | awk -F: '{print \$2}'", returnStdout: true).trim()
                            echo "The dynamically allocated host port is: ${hostPort}"

                            // Get the ID of the agent container
                            def agentContainerId = sh(
                                script: "cat /proc/self/cgroup | grep 'docker' | sed 's/^.*\\///' | tail -n 1",
                                returnStdout: true
                            ).trim()

                            // Attach the agent container and the pulled image container to the custom network
                            echo "Connecting agent and pulled containers to the custom network"
                            sh "docker network connect ${NETWORK_NAME} ${agentContainerId}"
                            sh "docker network connect ${NETWORK_NAME} ${CONTAINER_NAME}"

                            // Inspect the containers inside the custom network
                            echo "Inspecting containers inside the custom network"
                            sh "docker network inspect ${NETWORK_NAME}"

                            // Construct the endpoint URL based on host and port
                            def endpointUrl = "http://${CONTAINER_NAME}:${env.PORT}/"
                            echo "Application endpoint URL: ${endpointUrl}"
                            env.PR_ENDPOINT_URL = endpointUrl
                        }
                    } else {
                         echo "Skipping ECR authentication and Docker operations - PR_DOCKER_IMAGE is empty or null"
                    }
                }
            }
        }

        stage('Feature Flag validation') {
            steps {
                script {
                    // Define a Groovy variable for the command, initialized with the value
                    // from environment
                    shCommand = env.SHCOMMAND
                        // Check for the selected CODE_VERSION
                        if (params.CODE_VERSION == 'v1' || params.CODE_VERSION == 'v2') {
                            // Check if CLIENT_SAMPLING is true
                            if (params.CLIENT_SAMPLING) {
                                if (params.CODE_VERSION == 'v1') {
                                    // v1 logic: Check and validate CLIENT_SAMPLING_FILENAMES
                                    if (params.CLIENT_SAMPLING_FILENAMES == '') {
                                        error("CLIENT_SAMPLING was enabled, but no filenames were provided in the 'CLIENT_SAMPLING_FILENAMES' parameter for version v1. Aborting the build.")
                                    } else {
                                        echo "Inside CLIENT_SAMPLING_FILENAMES shCommand"
                                        // Append client_sampling flag and client_sampling_filenames to the command for v1
                                        shCommand += " --client_sampling ${CLIENT_SAMPLING_FLAG} --client_sampling_filenames ${CLIENT_SAMPLING_FILENAMES}"
                                    }
                                } else if (params.CODE_VERSION == 'v2') {
                                    // v2 logic: Handle the new command addition for client sampling in v2
                                    if (params.CLIENT_SAMPLING_CLIENT_IDS == '') {
                                        error("CLIENT_SAMPLING was enabled, but no client ids were provided in the 'CLIENT_SAMPLING_CLIENT_IDS' parameter for version v2. Aborting the build.")
                                    } else {
                                        // Append client_sampling flag and client_sampling_client_ids to the command for v1
                                        shCommand += " --client_sampling ${CLIENT_SAMPLING_FLAG} --client_sampling_client_ids ${CLIENT_SAMPLING_CLIENT_IDS}"
                                    }
                                }
                            } else {
                                echo "CLIENT_SAMPLING was not enabled. Skipping this feature."
                            }
                        } else {
                            error("Invalid CODE_VERSION selected. Must be 'v1' or 'v2'. Aborting the build.")
                        }
                        // Check if REQUEST_SAMPLING is true and validate REQUEST_SAMPLING_COUNT
                        if (params.REQUEST_SAMPLING) {
                            if (params.REQUEST_SAMPLING_COUNT.trim() == '') {
                                error("REQUEST_SAMPLING was enabled, but no request sampling count was provided in the 'REQUEST_SAMPLING_COUNT' parameter. Aborting the build.")
                            } else if (params.REQUEST_SAMPLING_COUNT.toInteger() < 1) {
                                // Ensure that the REQUEST_SAMPLING_COUNT is an integer and greater than or equal to 1
                                error("REQUEST_SAMPLING_COUNT must be greater than or equal to 1. Aborting the build.")
                            } else {
                                // Append request_sampling flag and request_sampling_count to the command
                                shCommand += " --request_sampling ${REQUEST_SAMPLING_FLAG} --request_sampling_count ${REQUEST_SAMPLING_COUNT}"
                            }
                        } else {
                            echo "REQUEST_SAMPLING was not enabled. Skipping this feature."
                        }
                        // update the shCommand for ENABLE_SCORE_ARCHIVE
                        shCommand += " --enable_score_archive ${ENABLE_SCORE_ARCHIVE}"
                }
            }
        }
        stage('Build Dependencies') {
            steps {
                    echo "###########  Install the requirements ########### "
                    sh 'pip3 install --upgrade pip'
                    echo "pip3 install -r ./requirements.txt"
                    sh 'pip3 install -r ./requirements.txt'
                    echo "Build Completed and requirement installed successfully"
            }
        }
        stage('Automated Test') {
            steps {
                echo " ########### Running Automated Test ###########"
                echo " ########### pytest -v -s ${TESTS_DIR} --env ${ENV} --reruns ${MAX_RUNS} --maxfail ${MAX_FAIL} ########### "
                sh "${shCommand}"
                // Ensure correct permissions for allure-results
                sh "chmod -R 777 allure-results"
                echo " ########### ${ENV} Automated Tests completed successfully ###########"
                 // Exit the pipenv virtual environment
                sh 'exit'
            }
        }

    }
post {
    always {
        script {
            // Ensure allure results directory has proper permissions
            sh "chmod -R 777 ${WORKSPACE}/allure-results"

            // Clean up Docker resources if any
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker rm ${CONTAINER_NAME} || true"
            sh "docker container prune -f || true"
            //List all containers connected to a network and disconnect them
            sh "docker network inspect ${NETWORK_NAME} -f '{{range .Containers}}{{.Name}}{{end}}' | xargs -r docker network disconnect ${NETWORK_NAME}"
            // Remove the specific image we used previously if no longer needed
            sh "docker rmi ${DOCKER_IMAGE} || true"

            // Clean up custom Docker network
            sh "docker network rm ${NETWORK_NAME} || true"
            sh "docker system prune -f || true"
            sh "docker network ls"

            // Generate Allure report
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            // Publish JUnit test results
            junit 'pytest-report.xml'

            // Publish HTML test report
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'pytest-report.html',
                reportName: 'Pytest Report'
            ])
            // Clean up workspace
            cleanWs()
        }
    }

    success {
        script{
                env.TRIGGERED_BY = env.BUILD_USER ?: env.BUILD_USER_ID ?: env.UPSTREAM_BUILD ?: 'CRON Job'
                echo "upstream build: ${env.UPSTREAM_BUILD}"
                echo "Build cause: ${env.BUILD_CAUSE}"
                echo "Build triggered by: ${env.TRIGGERED_BY}"
//                 sendNotification('Success', '#7CFF5A', 'Build successful')
            }
    }
    failure {
        script{
                env.TRIGGERED_BY = env.BUILD_USER ?: env.BUILD_USER_ID ?: env.UPSTREAM_BUILD ?: 'CRON Job'
                echo "Build triggered by: ${env.TRIGGERED_BY}"
//                 sendNotification('Failure', '#E10000', 'Build failed. Take another crack?')
            }
    }
    unstable {
        script{
                env.TRIGGERED_BY = env.BUILD_USER ?: env.BUILD_USER_ID ?: env.UPSTREAM_BUILD ?: 'CRON Job'
                echo "Build triggered by: ${env.TRIGGERED_BY}"
//             sendNotification('Unstable', '#FFFF00', 'Build unstable. Take another crack?')
        }
    }
    }
}