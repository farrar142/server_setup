가정
HOST :AWS EC2 Red Hat Enterprise Linux 8 (HVM)

### EC2 REDHAT 64bit x86

도커버전 : 20

젠킨스는 꼭 도커로 설치

### 호스트 shell

1. sudo yum install git -y && sudo mkdir /home/${USER}/Tutorial && cd /home/${USER}/Tutorial && sudo git clone https://github.com/farrar142/jenkins_tutorial . && sudo python3 py_installer.py && cd /home/${USER}/Tutorial/jenkins && sudo docker-compose up -d
2. localhost:8080 으로 접속

### 젠킨스 shell

docker exec -it jenkins /bin/bash
cat /var/jenkins_home/secrets/initialAdminPassword == 초기비밀번호

### 젠킨스 페이지에서 플러그인들 설치.

### 사용자 계정 생성

### 젠킨스 기본설치

# 문제

## 문제 1

목표 : 아이템 등록 후, 수동빌드, 파일 생성

http://${hostip}:8080

1. 새로운 item -> jenkins_tutorial ,freestyle project -> 시작 ->
2. 빌드 -> execute shell

#### COMMAND

```

mkdir folder_name

```

3. 저장-> build now -> ls /var/jenkins_home/workspace/jenkins_tutorial ->
4. folder_name이 나와야 정상.

## 문제 2

목표 : 파일 생성 후 삭제

1. jenkins_tutorial 아이템 -> 구성
2. 빌드 -> execute shell

```
mkdir something
rm -rf $(ls)
```

3. 저장 ->build now
4. 컨테이너 안에서 ls /var/jenkins_home/workspace/jenkins_tutorial
5. 아무것도 나오지 않으면 성공.

## 문제 3

목표 : 젠킨스에서 외부파일 가져오기

1. 로컬에서 git 리포지터리와 연동 할 폴더 생성 후
2. 로컬과 깃허브 연동
3. docker-compose.yml 생성

##### 사용예제

docker-compose.yml

```

version: "3"

services:
  python:
    image: python:latest
    container_name : python
    volumes:
        - .:/usr/src/app

```

#### COMMAND

```
git clone 개인_리포지터리 .
```

#### 젠킨스 shell

```

ls /var/jenkins_home/workspace/jenkins_tutorial
docker-compose.yml 확인

```

## 문제 4

목표 : 이미지 생성 및 실행

#### COMMAND

```
docker pull python:latest
docker run -d --name python python:latest
.             {컨테이너 이름}{이미지이름}
```

## 문제 5

목표 : 이미지 생성 및 기존 이미지 삭제
단 jenkins컨테이너는 종료하면 안됨

#### COMMAND

```

docker rm -f python
docker rmi -f python

```

## 문제 6

목표 : 이미지 생성 및 로컬에서 접속

#### https://github.com/farrar142/jenkins_tutorial

1. 예제를 다운로드하여 in_docker폴더를 개인 리포지터리에 복사,붙여넣기

#### COMMAND

```
git pull
cd in_docker
docker build --tag test:0.1 .
docker run -d --name python1 -p 8000:8000 test:0.1
```

## 문제 7

목표 : 새 이미지 빌드, 기존 컨테이너 끄기, 새 이미지로 새 컨테이너 실행, 기존 이미지 삭제

#### COMMAND

```
git pull
cd in_docker
docker build --tag test:0.2 .
docker stop python1
docker run -d --name python2 -p 8000:8000 test:0.2
docker rm -f python1
docker rmi -f test:0.1
```

## 문제 8

목표 : ngrok 설치하여, 로컬PC를 외부에서 접근할 수 있도록

##### ngrok 설치 방법이 다양하여 도커로 통일.

1. 장고 기준 in_docker/django_server/settings.py 에서 ALLOWED_HOSTS = ["*"]로 바꿔줌.
2. https://dashboard.ngrok.com/get-started/setup 회원가입 후
3. https://dashboard.ngrok.com/get-started/your-authtoken 키 획득

```
docker run --net=host --name ngrok -ite NGROK_AUTHTOKEN={여기에 붙여넣으세요} ngrok/ngrok http 8080
```

#### COMMAND

```
git pull
cd in_docker
docker build --tag test:0.3 .
docker stop python2
docker run -d --name python3 -p 8000:8000 test:0.3
docker rm -f python2
docker rmi -f test:0.2
```

5. gnrok에서 주어진 http 주소로 접속.

## 문제 9

목표 ssh 키를 생성하여, public 키를 깃허브에 등록하고, private 키를 젠킨스에 등록

깃허브에 커밋이 발생하면, 아이템 실행하여 간단한 파일 생성

1. mkdir /var/jenkins_home/.ssh
2. cd /var/jenkins_home/.ssh
3. ssh-keygen -t rsa -b 4096 -C tutorial -f git_jenkins
4. cat git_jenkins 나온 내용을 localhost:8080 젠킨스 사이트 접속
5. jenkins 관리 -> Security -> Manage Credentials -> global -> add credentials
6. kind를 SSH Username with private key로 변경
7. Username 설정
8. private key -> Enter directly -> add
9. cat git_jenkins의 내용을 입력
10. 개인 깃허브 리포지터리 접속 -> settings -> deply keys -> Add deploy key -> Title 설정 Key ->cat git_jenkins.pub 의 내용을 입력
11. 깃허브 리포지터리 -> settings -> Webhooks -> Add webhook
12. jenkins의 주소/github-webhook/
13. add webhook
14. jenkins 새로운 아이템 생성
15. 소스코드 관리 -> git
16. repository url = git의 ssh주소, 리포지터리 메인화면의 초록색 버튼에 있어요.
17. 빌드유발 -> GitHub hook trigger for GITScm polling
18. build -> Execute shell

#### COMMAND

```
mkdir web-hook-test
```

19. 깃허브의 리포지터리에 아무 파일이나 push 후
20. 젠킨스의 빌드가 진행되고
21. ls /var/jenkins_home/workspace/jenkins_tutorial에서 web-hook-test 폴더가 나와야 성공.

## 문제 10

목표 이전 컨테이너 삭제 후, 새 컨테이너 실행

이전 문제의 build 창에서

#### COMMAND

```
git pull
cd in_docker
docker rm -f python3
docker run -d --name python4 -p 8000:8000 test:0.3
```

#### 젠킨스 shell

```
docker ps -a 명령으로 python4 컨테이너가 생성되었는지 확인
```
