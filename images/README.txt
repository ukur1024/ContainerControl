/etc/default/docker добавить опцию:
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4 -g /new/location"
где /new/location - текущая.