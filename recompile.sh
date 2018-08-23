# shell script to re-build my project while docker is pointing to the
# local machine (use the local shell), and publish to the repository
cd /home/dave/docker
docker build --no-cache -t friendlyhello .
docker tag friendlyhello dave4mpls/get-started:part2
docker push dave4mpls/get-started:part2

