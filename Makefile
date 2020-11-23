DOCKER_NETWORK = docker-hadoop_default
ENV_FILE = hadoop.env
current_branch := $(shell git rev-parse --abbrev-ref HEAD)
build:
	docker build -t covid2020/hadoop-base:$(current_branch) ./base
	docker build -t covid2020/hadoop-namenode:$(current_branch) ./namenode
	docker build -t covid2020/hadoop-datanode:$(current_branch) ./datanode
	docker build -t covid2020/hadoop-resourcemanager:$(current_branch) ./resourcemanager
	docker build -t covid2020/hadoop-nodemanager:$(current_branch) ./nodemanager
	docker build -t covid2020/hadoop-historyserver:$(current_branch) ./historyserver
	docker build -t covid2020/hadoop-submit:$(current_branch) ./submit

covidscraper:
	docker build -t hadoop-covidscraper ./submit
	docker run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} covid2020/hadoop-base:$(current_branch) hdfs dfs -mkdir -p /input/
	docker run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} covid2020/hadoop-base:$(current_branch) hdfs dfs -copyFromLocal -f /opt/hadoop-3.2.1/README.txt /input/
	docker run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} hadoop-covidscraper
	docker run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} covid2020/hadoop-base:$(current_branch) hdfs dfs -cat /output/*
	docker run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} covid2020/hadoop-base:$(current_branch) hdfs dfs -rm -r /output
	docker run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} covid2020/hadoop-base:$(current_branch) hdfs dfs -rm -r /input