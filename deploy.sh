#shell script to load the changes from the repository and deploy them
#to the AWS swarm
cd /home/dave/docker
docker pull dave4mpls/get-started:part2
docker stack deploy -c docker-compose.yml getstartedlab

