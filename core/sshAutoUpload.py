import paramiko
import socket
from scp import SCPClient
import json
import os
import re
import time
import logging
logger = logging.getLogger(__name__)

def ssh_auto_upload(host, port, user, password, local_path, remote_path, enableRestart):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:

        # 找UUID
        uuid = find_uuid_in_json(local_path)
        if(uuid == ""):
            return False
        
        # 连接
        ssh.connect(
            host,
            port=port,
            username=user,
            password=password,
            timeout=10,
            banner_timeout=10,
            auth_timeout=10
        )
        scp = SCPClient(ssh.get_transport())

        # 上传
        logger.info("正在使用SSH上传")
        stdin, stdout, stderr = ssh.exec_command(f"mkdir {remote_path}/{uuid}")
        upload_dir(scp, ssh, local_path, f"{remote_path}/{uuid}")
        logger.info("上传完成")
        if enableRestart:
            stdin, stdout, stderr = ssh.exec_command("pidof epass_drm_app")
            stdin, stdout, stderr = ssh.exec_command(f"kill {stdout.read().decode().strip()}")

            # 某个神秘应用退出的时候磨磨蹭蹭（）（）（）（）
            start_time = time.time()
            while True:
                stdin, stdout, stderr = ssh.exec_command("pidof epass_drm_app")
                if (not (stdout.read().decode().strip().isdigit())):
                    logger.info("主程序已退出")
                    break
                if time.time() - start_time > 15:
                    logger.error("等待程序退出超时，可能需要手动重启通行证上的程序")
                    return False
                time.sleep(0.5)
            
            stdin, stdout, stderr = ssh.exec_command("nohup /root/epass_drm_app > output.log 2>&1 &")


    except socket.timeout:
        logger.error("连接或执行命令超时")
        return False

    except paramiko.ssh_exception.NoValidConnectionsError:
        logger.error("SSH端口无法连接")
        return False

    except paramiko.ssh_exception.AuthenticationException:
        logger.error("SSH认证失败")
        return False

    except paramiko.SSHException as e:
        logger.error("SSH错误:", e)
        return False

    finally:
        scp.close()
        ssh.close()


def find_uuid_in_json(path):
    """
    在指定的path下查找*.json文件（只会查找一次），找到后返回uuid字段，仅包含字母、数字和连字符，失败返回空文本
    """
    try:
        if not os.path.isdir(path):
            return ""
        
        # 查找.json文件
        json_files = [f for f in os.listdir(path) if f.endswith('.json')]
        if not json_files:
            return ""
        
        # 只取第一个.json文件
        json_file = json_files[0]
        json_path = os.path.join(path, json_file)
        
        # 读取并解析JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        uuid_raw = data.get('uuid', '')
        
        # 过滤，只保留字母、数字和连字符
        uuid_clean = re.sub(r'[^a-zA-Z0-9\-]', '', uuid_raw)
        return uuid_clean
    
    except Exception:
        return ""

def upload_dir(scp: SCPClient, ssh, local_dir: str, remote_dir: str):
    """
    上传 local_dir 下的所有文件和文件夹到 remote_dir。
    """
    if not os.path.isdir(local_dir):
        raise ValueError(f"{local_dir} 不是有效目录")

    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"
        
        if os.path.isfile(local_path):
            scp.put(local_path, remote_path=remote_path)
        elif os.path.isdir(local_path):
            # 创建远程目录
            ssh.exec_command(f"mkdir -p {remote_path}")
            # 递归上传子目录
            upload_dir(scp, ssh, local_path, remote_path)