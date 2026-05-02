FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y     python3 python3-pip python3-venv git curl ca-certificates     && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/ROS2-Agent
COPY . /workspace/ROS2-Agent
RUN python3 -m pip install --upgrade pip && pip3 install -r requirements-dev.txt
CMD ["bash"]
