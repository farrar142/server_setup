import os


centos_list = [
    "sudo yum install yum-utils device-mapper-persistent-data lvm2 -y",
    "sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
    "sudo yum install docker-ce -y",
    "sudo yum install curl -y",
    "sudo curl -L \"https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
    "sudo chmod +x /usr/local/bin/docker-compose",
    "sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose",
    "sudo groupadd docker",
    "sudo usermod -aG docker ${USER}",
    "sudo systemctl start docker",
    "sudo systemctl daemon-reload",
    "sudo systemctl enable docker",
    "sudo systemctl enable containerd.service",
    "sudo chmod 666 /var/run/docker.sock",

]
# 인스톨기능


def install(list):
    for i in list:
        print(f"\n{i}\n")
        os.system(i)


def install_centos():
    print("튜토리얼 환경 설치")
    install(centos_list)


if __name__ == "__main__":
    install_centos()
