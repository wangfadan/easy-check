#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
import subprocess, os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def run_command(cmd, shell=False):
    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=shell, env=env)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

@app.route("/run_cpu", methods=["POST"])
def run_cpu():
    cmd = [
        "ansible",
        "-i", "/opt/kolla_installer/ceph-deploy/inventory/machines",
        "openstacks",
        "-m", "shell",
        "-a", "mpstat 1 1 | tail -1 | awk '{printf(\"%0.2f\\n\", 100-$12)}'",
        "-e", "ansible_python_interpreter=/usr/bin/python3"
    ]

    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)

 
# 内存
@app.route("/run_mem", methods=["POST"])
def run_mem():
    cmd = [
        "ansible",
        "-i", "/opt/kolla_installer/ceph-deploy/inventory/machines",
        "openstacks",
        "-m", "shell",
        "-a", "free -h | awk '/Mem/ {print $4}'",
        "-e", "ansible_python_interpreter=/usr/bin/python3"
    ]    
    
 
    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)


# 根分区情况
@app.route("/run_disk", methods=["POST"])
def run_disk():
    cmd = [
        "ansible",
        "-i", "/opt/kolla_installer/ceph-deploy/inventory/machines",
        "openstacks",
        "-m", "shell",
        "-a", "df -h / | awk 'NR==2 {print $5}'",
        "-e", "ansible_python_interpreter=/usr/bin/python3"
    ]

    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)

 
# osd使用情况
@app.route("/run_osd", methods=["POST"])
def run_osd():
    cmd = [
        "ansible",
        "-i", "/opt/kolla_installer/ceph-deploy/inventory/machines",
        "openstacks",
        "-m", "shell",
        "-a", "df -h | awk -F ' ' '/^\\/dev/ {print $5, $NF}'",
        "-e", "ansible_python_interpreter=/usr/bin/python3"
    ]

    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)


# 系统负载使用情况
@app.route("/run_systemload", methods=["POST"])
def run_systemload():
    cmd = [
        "ansible",
        "-i", "/opt/kolla_installer/ceph-deploy/inventory/machines",
        "openstacks",
        "-m", "shell",
        "-a", "uptime",
        "-e", "ansible_python_interpreter=/usr/bin/python3"
    ]

    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)


# docker服务情况
@app.route("/run_dok", methods=["POST"])
def run_dok():
    cmd = [
        "ansible",
        "-i", "/opt/kolla_installer/ceph-deploy/inventory/machines",
        "openstacks",
        "-m", "shell",
        "-a", "docker ps -a |grep -v Up",
        "-e", "ansible_python_interpreter=/usr/bin/python3"
    ]

    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)

# ceph服务情况
@app.route("/run_cep", methods=["POST"])
def run_cep():
    cmd = ["ceph", "-s"]

    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)

# ceph服务情况
@app.route("/run_mql", methods=["POST"])
def run_mql():
    cmd = ["galera-status"]

    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)

#nova服务
@app.route("/run_nova", methods=["POST"])
def run_nova():
    cmd = [
      "bash", "-c",
       """
       source /root/.admin-openrc.sh &&
        nova service-list | awk -F'|' '
       NR>2 && $2 !~ /^-+/ {
        gsub(/^ +| +$/, "", $3);
        gsub(/^ +| +$/, "", $4);
        gsub(/^ +| +$/, "", $5);
        gsub(/^ +| +$/, "", $6);
        gsub(/^ +| +$/, "", $7);
        printf "%-18s %-12s %-10s %-8s %-6s\\n",
               $3, $4, $5, $6, $7
      }'
      """
    ] 


    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)

#cinder服务
@app.route("/run_cinder", methods=["POST"])
def run_cinder():
    cmd = [
        "bash", "-c",
          """
         source /root/.admin-openrc.sh &&
         cinder service-list | awk -F'|' '
         NR>2 && $2 !~ /^-+/ {
        gsub(/^ +| +$/, "", $3);
        gsub(/^ +| +$/, "", $4);
        gsub(/^ +| +$/, "", $5);
        gsub(/^ +| +$/, "", $6);
        gsub(/^ +| +$/, "", $7);
        printf "%-18s %-12s %-10s %-8s %-6s\\n",
                $3, $4, $5, $6, $7
       }'
       """
    ]
    env = os.environ.copy()
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "执行失败: {}".format(e)

    return jsonify(result=output)



if __name__ == "__main__":
    app.run(host="192.168.8.204", port=7000)
