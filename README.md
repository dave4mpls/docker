# Docker Example
### Candidate: Dave White, dave 4 mpls [at] gmail [dot] com, 612-695-3289
### Position: Guest Reliability Engineer

Live Demo is at: [http://myloadbalancer-1065778686.us-east-2.elb.amazonaws.com/](http://myloadbalancer-1065778686.us-east-2.elb.amazonaws.com/)

Since I didn't have knowledge of containerization and Docker during the interview, I decided to learn about it today.  Therefore, this is a good example of my independent learning process: yesterday the only thing containerization brought to mind was ships delivering large metal boxes across the Pacific Ocean, and today I have a load-balanced Docker swarm running on two virtual machines inside of Amazon Web Services EC2 (my knowledge of AWS EC2 yesterday was "I've heard of it.")

I started by googling, of course, and then went through the Docker tutorial, which this project is based on.  The tutorial showed me how to create a simple web page in Python, using Flask to serve the pages, and put the program and all its dependencies (Python, Flask) in a container that could run anywhere.  I ran it on my local machine (actually a Linux VM) and then installed it in AWS where it ran on two load-balanced Virtual Machines.  The tutorial also showed how to share state between multiple load-balanced instances, by creating a visitor counter using Redis that only ran on one VM within the swarm and provided services over TCP/IP to the other one.

I mentioned that I learn best by creating something more complicated than the tutorial, and that is the case here: I expanded the tutorial project to add my NextBus Python module from the Target Case Study, so that it can run in AWS and contact the Metro Transit API to display bus information.  This required adding some Python dependencies to the container.  I then added a whole new Docker service, MySQL, which had to run on only the swarm manager so that its database can be accessed by any of the instances.  The database is used to record all the different bus queries that have been made so far, so they can be easily recalled.

To use the live load-balanced instance on AWS click on this link: [http://myloadbalancer-1065778686.us-east-2.elb.amazonaws.com/](http://myloadbalancer-1065778686.us-east-2.elb.amazonaws.com/).

The code files that I used are in this GitHub repository.

