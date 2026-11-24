pipeline {
  agent any
  environment {
    IMAGE = 's2025tm93013/aceest-fitness'
    TAG   = "${BUILD_NUMBER}"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Test & Coverage') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements-dev.txt
          python -m pytest --cov=app --cov-report=xml:coverage.xml -q
        '''
      }
    }
    stage('SonarQube Analysis') {
      steps {
        script { scannerHome = tool 'SonarScanner' }
        withSonarQubeEnv('SonarQube') {
          sh '/opt/sonar-scanner/bin/sonar-scanner'
        }
      }
    }
    stage('Quality Gate') {
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }
    stage('Docker Build & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
            usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            docker build -t $IMAGE:$TAG -t $IMAGE:latest .
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push $IMAGE:$TAG
            docker push $IMAGE:latest
          '''
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          kubectl set image deployment/aceest-fitness aceest-fitness=$IMAGE:$TAG
          kubectl rollout status deployment/aceest-fitness --timeout=120s || {
            kubectl rollout undo deployment/aceest-fitness
            exit 1
          }
        '''
      }
    }
  }
  post {
    always { sh 'docker logout || true' }
  }
}