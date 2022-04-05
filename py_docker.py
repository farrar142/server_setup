import os
import locale
import subprocess


def get_logs(cmd):
    os_encoding = locale.getpreferredencoding()
    #print("System Encdoing :: ", os_encoding)
    if os_encoding.upper() == 'cp949'.upper():  # Windows
        return subprocess.Popen(
            cmd, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    elif os_encoding.upper() == 'UTF-8'.upper():  # Mac&Linux
        return os.popen(cmd).read()
    else:
        print("None matched")
        exit()


def get_ports_from_strings(_result, words):
    try:
        tcp = words[-2].split("->")
        _tcp = ""
        for strings in tcp:
            if "tcp" in strings:
                _tcp = strings
                break
        return _tcp.split("/")[0]
    except:
        return ""


def get_docker_imgs():
    cmd = "docker images"
    logs = get_logs(cmd).split("\n")
    column = logs.pop(0)
    result = []
    if logs:
        for line in logs:
            if line:
                words = line.split(" ")
                while '' in words:
                    words.remove('')
                result.append([words[0], words[2]])
    return result


def get_docker_containers():
    cmd = "docker ps -a"
    logs = get_logs(cmd).split("\n")
    column = logs.pop(0)
    result = []
    if logs:
        for line in logs:
            words = line.split("  ")

            while '' in words:
                words.remove('')

            for i in range(len(words)):
                words[i] = words[i].strip().strip()
            try:
                status = words[4].strip().split(" ")[0]
                # print(f"C Name :: {words[-1]}, C ID :: {words[0]}, Img Name :: {words[1]} , Status :: {status}")
                _result = [words[-1], words[0], words[1], status]
                # 실행중이면 ports값도 얻어내옴
                _result.append(get_ports_from_strings(_result, words))
                # 인스턴스 ip 주소값도 알아내옴.
                _result.append(get_logs(
                    "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "+words[0]).strip("'"))
            except:
                _result = []
            result.append(_result)
    else:
        print("No Containers")
    return result


def get_informs():
    """
    cname,cid,imgname,status,port,ip
    """
    imgs = get_docker_imgs()
    container = get_docker_containers()
    for i in container:
        for j in imgs:
            try:
                cur = i[2].split(":")[0]
            except:
                cur = i[2]
            if j[0] == cur:
                i = i.insert(3, j[1])
                break
    return container


strFormat = '\n%-20s%-15s%-10s%-15s%-10s%-7s%-10s'

if __name__ == "__main__":
    containers = get_informs()
    print(strFormat % ("ContainerName", "ContainerID",
          "ImgName", "ImageID", "Status", "Port", "IP"))
    for i in containers:
        print(strFormat % (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
