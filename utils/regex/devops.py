devops_skill_regex = r"gcp|ecs|cicd|ci/cd|pipeline|artifactory|spring batch|elasticsearch|boto3|elasticache|terraform|codepipeline|facade|sqs \(simple queue service\)|capistrano|agile|microservices apis|kubernetes|pivotal cloud foundry|fargate|telegraf|consul|synopsys hub|google cloud platform|circleci|docker swarm|aws cloud services|kafka|ansible|aws vpc \(virtual private cloud\)|azure automatedml|tcp/ip|azure hub|aws cloudformation|kibana|bash|redshift|hashicorp|docker|ci/cd \(continuous integration/continuous deployment\)|load balancer|microsoft cloud|luigi|elastic beanstalk|aks \(azure kubernetes service\)|chef|azure functions|gke \(google kubernetes engine\)|packer|jwt token|bamboo|condor|airflow|cloudwatch|azure service|hadoop|argo cd|gitflow|salt|buildah|microsoft gpo \(group policy object\)|kubernetes|clang|aurora|oci \(oracle cloud infrastructure\)|cloudfront|podman|aws cloud|bicep|elb \(elastic load balancer\)|amazon emr \(elastic mapreduce\)|ecs \(elastic container service\)|kubernetes clusters|mlops \(machine learning operations\)|azure event hub|jaeger|udp \(user datagram protocol\)|azure ad \(active directory\)|arm templates|nginx|aws s3 \(simple storage service\)|maven|aws cdk \(cloud development kit\)|op5|sd-wan|bitbucket|aws networking services|azure databricks|fastlane|appdynamics|dast \(dynamic application security testing\)|autosys|aws iam \(identity and access management\)|dhcp \(dynamic host configuration protocol\)|aws cloudfront|iac \(infrastructure as code\)|microservices|sns \(simple notification service\)|openstack|azure devops|route 53|ml engineer \(machine learning engineer\)|splunk|rancher|pivotal cloud foundry|eks \(elastic kubernetes service\)|code magic|codebuild|docker compose|app services|ci/cd pipeline|mlflow|fortify|azure services|iam \(identity and access management\)|bitrise|checkmarx|tfs \(team foundation server\)|elk \(elasticsearch, logstash, kibana\)|google cloud|databricks|ci/cd \(continuous integration/continuous deployment\)|spring contract|aws rds \(relational database service\)|gce \(google compute engine\)|vpc \(virtual private cloud\)|aws cloudwatch|aws networking|paas \(platform as a service\)|azure bus \(service bus\)|pulumi|prometheus|aws batch|aws serverless|docker compose|ebs \(elastic block store\)|jenkins|soap api|cli \(command line interface\)|istio|t-sne \(t-distributed stochastic neighbor embedding\)|kubernetes|fastlane|rds \(relational database service\)"

devops_regex = [
    {
        'tech_stack': 'Devops',
        'exp': '(?i)(^|\W)(dev[-\s]?ops|azure|deployment|CI[-\/\s]?CD|Continuous[-\s]Integration|Release[-\s]Engineer|Systems?[-\s]Engineer|Cloud[-\s](Developer|Engineer)|Infrastructure Engineer|aws|Operations Engineer|Amazon Web Services|Google[-\s]?Cloud|Apache|Nginx|Gunicorn|Docker|Kubernetes|lambda|EC2|Elastic[-\s]Search|Kibana|S3|Cloud[-\s]Watch|Cloud[-\s]?(Infrastructure|Platform|formation))(\W|$)'
    },
]
