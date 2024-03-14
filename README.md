# Data-Engineering1-Project
This project's aim was to deploy a scalable data processing solution and analyze a data set. 

Our solution was to deploy a Spark cluster for performing the computations and HDFS for storing the data.
We automated the solution by a script start.py to launch new virtual machines, set_up_worker.sh to configure new workers and data nodes on the cluster.
Additionally stop.py will remove a worker and we can look up availble ips with checkip.py.

The datanalyze was performed on the Webis-TLDR-17 Corpus dataset of Reddit posts. The questions we wanted to examine the dataset were:

     Which are the most popular subreddits?
     What are the most frequently occurring words?
     What are the authors using the most amount of bad words?
     What are the most frequent occurring words of the most popular subreddits?

Additionally we wanted to test the strong scalability of the solution. This together with the data anlaysis can be found in the Experiments folder. 
