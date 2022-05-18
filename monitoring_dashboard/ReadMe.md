## These are code samples for a monitoring dashboard. 

### Requirement for this dashboard:
- We had approximately 10 environmets with same Infrastructure Configurations, deployed on AWS. 
- Each environment had the following EC2 instances running core application components:
    - Two EC2 instances dedicated for Front End services (App Servers)
    - Two EC2 instances dedicated for Backend APIs (API Servers)
    - One EC2 instance dedicated for an authentication app (Perry Server)
    - Additional EC2 instances running other applications like Elasticsearch, Rundeck and Jenkins Slave.

---

Each core component was deployed as a docker container on two EC2 instances for High Availability except for Perry, the authentication service, which was running on just one EC2 instance.

We were in the early stage of our project and did not have any monitoring tools set up. As a result, the Development teams often used to reach out to the DevOps team complaining that their applications are not available. When DevOps team investigated, we found that the docker containers for that application was in *exited* status. 

This was an embarrasment for the DevOps team as we should have been alerted whenever a docker container went down. Instead, we only found out about this when the Development team complained about applications not running. 

---

As a quick workaround, our managers enforced a rule for every DevOps engineer on-call to manually SSH into each EC2 instance and run `docker ps -a` command to catch any docker containers in *exited* state. 

This was obviously not a feasible solution, as the on-call engineer had to manually run this command on each EC2 instance across all 10 environments. We failed badly at this approach. 

I was not comfortable with this manual approach and spent some time to write an Ansible script that would run the `docker ps -a` command on all EC2 instances in all environments and return the output as stdout to the the terminal. 

This script was very useful and greatly reduced the manual efforts. Now, the on-call DevOps engineer only had to run the Ansible command to run the playbook and they could get the status of all docker containers from all environments. 

My managers praised this automation script a lot and pushed me to design a solution that would show this information in real time in the form of a Dashboard. 

---

### Dashboard Design

For the Dashboard design, I came up with the following solution:

- Run the `docker ps -a` command on each EC2 host and capture this output in a comma separated text file.
- Crated a Python script that would parse this comma separated text file and dynamically generate HTML files with EC2 hostname, Docker Container name, Docker Container Status and Docker Image version deployed. 
- Once the HTML files are generated, they are pushed to an S3 bucket with `Static Webhosting` enabled.
- The Static website hosted on S3 served as the Monitoring Dashboard for Docker Container Status.

---

The `cwds-dash.yml` file is the master Ansible playbook which does the heavy lifting. Here is a summary of the tasks performed by this script:
- It runs the `docker ps -a` command on EC2 instances in all environmetns and saves the result in each environment's individual text file on that environment's Jenkins Slave instance. 
- Removes any existing environment text files present on the Master and collects all the individual environment text files present on the Jenkins Slave node and pulls them on the Master Jenkins instance. 
- Once the text files are collected on the Master Jenkins instance from all the Jenkins Slave nodes, it creates empty HTML files and copies the Python scripts to parse these text files. 
- Runs the python scripts to parse the environmnet text files and based on the script logic, writes HTML code blocks to the empty HTML files created earlier.
- Once the HTML files are generated, these files are pushed over to the S3 bucket, with versioning enabled. 

The `cwds-dash.yml` playbook was converted to a Jenkins job which was auto-started every 5 minutes. Thus, collecting the `docker ps -a` info every 5 minutes from all environments and generating new HTML files based on the python script logic, and finally pushing these new HTML files to the static webhosting enabled S3 bucket. 

This is how the Dashboard was created and got refreshed every 5 minutes, reporting near-real time monitoring data for the status of all Docker Containers. 

---

## Python Script Code:

Each environment had its own Python script to parse the comma separated text file. I have added a sample Pyhon script file called `demo-int.py` for reference.

The Python script I created was all part of trial-and-error and therefore, does not follow any best practices for coding and naming conventions. While I was working on this project, I wrote the python scripts in a very rough and rudimentary manner. 

However, when the Dashboard became functional and was released to the Project at large, it quickly gained popularity and adoption. It became a source of truth for monitoring the health of core components and I did not get a chance to refactor the code and align it with best practices. 

---

## Demo Files:

I have uploaded the sample `demo-int.txt` and `demo-int.html` files here for reference. 

The `master-dash.html` file serves as the landing page for this dashboard. 
