pipeline {
    agent any 
    
    
    environment {
        GIT_REPOSITORY = "git@github.com:tranvannhan1911/minimart-server.git"
        DOCKER_REPOSITORY = "tranvannhan1911/minimart-server"
        CONTAINER_NAME = "minimart-server"
        DOCKERHUB_CREDENTIAL = credentials('dockerhub')
    }
    
    stages {
        stage("Checkout"){
            steps {
                script{
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "refs/heads/main"]],
                        extensions: [[$class: 'CleanCheckout']], // clean workspace after checkout
                        userRemoteConfigs: [[url: GIT_REPOSITORY, credentialsId: "git-minimart"]]])
                }
            }
        }
        
        stage("Test"){
            steps {
                script{
                    sh "python3 -m venv venv"
                    sh "source ./venv/bin/activate"
                    sh "pip install -r requirements.txt"
                    sh "python3 manage.py test"
                }
            }
        }
        
        stage("Code analysis with SonarQube"){
            steps{
                script{
                    def scannerHome = tool 'sonarqubescanner4.7';
                    withSonarQubeEnv('sonarqube') {
                      
                        sh """${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=minimart -Dsonar.sources=."""
                    }
                    
                    timeout(time: 10, unit: 'MINUTES'){
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }
        
        stage("Build docker image"){
            steps {
                script{
                    env.DOCKER_TAG = "v"+BUILD_NUMBER
                    env.DOCKER_REPOSITORY_TAG = DOCKER_REPOSITORY+":"+DOCKER_TAG
                    // appImage = docker.build DOCKER_REPOSITORY_TAG
                    sh 'docker build -t $DOCKER_REPOSITORY_TAG .'
                    
                }
                
            }
        }
        
        stage("Push image to docker hub"){
            steps {
                script{
                    // docker.withRegistry('', DOCKERHUB_CREDENTIAL){
                    //     appImage.push(DOCKER_TAG)
                    // }
                    sh 'echo $DOCKERHUB_CREDENTIAL_PSW | docker login -u $DOCKERHUB_CREDENTIAL_USR --password-stdin'
                    sh 'docker push $DOCKER_REPOSITORY_TAG'
                }
            }
        }
        
        stage("Deploy"){
            agent{
                label "minimart-server"
            }
            steps {
                script{
                    // sh 'echo $DOCKERHUB_CREDENTIAL_PSW | docker login -u $DOCKERHUB_CREDENTIAL_USR --password-stdin'
                    sh 'docker stop $CONTAINER_NAME || true'
                    sh 'docker rm $CONTAINER_NAME || true'
                    sh "docker rmi -f \$(docker images -a | grep '${DOCKER_REPOSITORY}' | awk '{print \$3}') || true"
                    sh '''docker run -d -p 8000:8000 \
                        -e MYSQL_NAME=$MYSQL_NAME \
                        -e MYSQL_USER=$MYSQL_USER \
                        -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
                        -e MYSQL_HOST=$MYSQL_HOST \
                        -e MYSQL_PORT=$MYSQL_PORT \
                        --restart on-failure:5 \
                        --name $CONTAINER_NAME \
                        $DOCKER_REPOSITORY_TAG'''
                }
                
            }
            post{
                success{
                    sh "docker exec $CONTAINER_NAME python3 manage.py migrate"
                }
            }
        }
    }
    post {
		always {
            cleanWs()
			sh "docker rmi $DOCKER_REPOSITORY_TAG"
            echo "cleaned"
            
            emailext(
                attachLog: true, 
                subject: "Minimart Server - Build #$BUILD_NUMBER - ${currentBuild.result}", 
                body: 'Build url: $BUILD_URL', 
                to: 'tranvannhan1911@gmail.com')
		}
	}
}