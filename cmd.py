# -*- coding:utf-8 -*-
from paramiko import AutoAddPolicy, RSAKey, SSHClient
import argparse
from pprint import pprint


def connectSshServerByPw(h, u, pw, cmd):
    c = SSHClient()
    c.set_missing_host_key_policy(AutoAddPolicy())
    c.connect(hostname=h, username=u, password=pw)
    commands = [cmd]
    for command in commands:
        print("Executing {}".format(command))
        _, stdout, stderr = c.exec_command(command)
        pprint(stdout.readlines())
        print("Errors")
        pprint(stderr.readlines())
    c.close()


def connectSshServerByFile(h, u, f, cmd):
    k = RSAKey.from_private_key_file(f)
    c = SSHClient()
    c.set_missing_host_key_policy(AutoAddPolicy())
    c.connect(hostname=h, username=u, pkey=k)
    commands = [cmd]
    for command in commands:
        print("Executing {}".format(command))
        _, stdout, stderr = c.exec_command(command)
        pprint(stdout.readlines())
        print("Errors")
        pprint(stderr.readlines())
    c.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ssh cmd", description="ssh 원격지 명령어")
    parser.add_argument("-H", "--host", dest="hostname", help="호스트 입력")
    parser.add_argument("-u", "--user", dest="username", help="사용자 입력")
    parser.add_argument("-c", "--cmd", dest="cmd", help="명령어 입력")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--key-file", dest="file",
                       help="접속 key 파일 위치 지정")
    group.add_argument("-p", "--password", dest="password", help="비밀번호 입력")

    args = parser.parse_args()
    hostname = args.hostname
    username = args.username
    file = args.file
    password = args.password
    cmd = args.cmd

    if file == None:
        connectSshServerByFile(hostname, username, file, cmd)
    elif password == None:
        connectSshServerByPw(hostname, username, password, cmd)
