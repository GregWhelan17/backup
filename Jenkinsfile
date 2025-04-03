pipeline {
    agent { label 'cm-linux' }
 
    stages {
        stage("Clone and checkout") {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: scm.branches,
                    extensions: scm.extensions, 
                    userRemoteConfigs: [[
                        credentialsId: scm.userRemoteConfigs[0].credentialsId,
                        name: 'origin', 
                        refspec: '+refs/heads/*:refs/remotes/origin/*', 
                        url: scm.userRemoteConfigs[0].url
                    ]],
                    doGenerateSubmoduleConfigurations: false
                ])
            }
        }
        stage('Authentication') {
            steps {
                withCredentials([usernamePassword(credentialsId: "service_acc_username_and_password", passwordVariable: 'password', usernameVariable: 'username')]) {
                    script {
                        kubectl_command = sh (
                            script: "curl -k -u ${username}:${password} -X GET https://oidc.${IKP_SERVER}.cloud.uk.hsbc/apitoken/token/user | jq -r '.token.\"kubectl Command\"'",
                            returnStdout: true
                        ).trim().replaceAll('\\$TMP_CERT','TMP_CERT').replaceAll(/export TMP_CERT=\$\(mktemp\) && /,'')
                        
                        output = sh (
                            script: kubectl_command,
                            returnStdout: true
                            ).trim()
                        println "Output after the command is run : $output"
                    }
                }
            }
        }
        stage('Backup Turbonomic') {
            steps {
                script {
                    println "Kubectl command in seperate stage:"
                    sh """kubectl config set-context --current --namespace=turbonomic"""
                    sh """pwd"""
                    sh """chmod a+x *.sh ; ./create_backup_job.sh"""
                    sh """echo ********BACKUP DONE******* """
                }
            }
        }
    }
}
