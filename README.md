# set_cloudwatch_logs_expire

terraform template for creating lambda and others resources to set cloudwatch expires as you wish. If you don't want to use terraform, you refer to "Lambda" directory.

## Getting Started

### Prerequisites

```
terraform >= 0.12.5
python >= 3.x
```
Terrafrom install guide: [Installing Terraform](https://learn.hashicorp.com/terraform/getting-started/install.html)

## Installing

```
$ git clone https://github.com/Sunochi/set_cloudwatch_logs_expire.git
```

### deployment to your AWS account

Use IAM User or Role that can create an IAM role.

```
## Set env variabel
$ export TF_VAR_lambda_function_name=stop_ec2_instances
$ export AWS_REGION=<any region name>

## Set your IAM info.
$ export AWS_SDK_LOAD_CONFIG=1
$ export AWS_PROFILE=<your aws profile>
## or
$ export AWS_ACCESS_KEY_ID=<access key>
$ export AWS_SECRET_ACCESS_KEY=<secret access key>

## create IAM resources.
$ cd IAM/
$ terraform init
$ terraform plan
$ terraform apply

## create Lambda resources.
$ cd Lambda/
$ ./lambda_build.sh
$ terraform init
$ terraform plan
$ terraform apply
```

#### CloudWatch Events

If you set cron events, deploy CloudWatch directory.
Run monthly by default.
```
$ cd CloudWatch/
$ terraform init
$ terraform plan
$ terraform apply
```

### Using

Default target region: ap-northeast-1  
To change region, you set environment value "TARGET_AWS_REGION".

### Delete Resources

Do in each directories.
```
$ terraform destroy
```

### Python Code Testing

Use testing tool [nose](https://nose.readthedocs.io/en/latest/).
In Lambda directory, run this command.
```
$ nosetests test_lambda_function.py  -v --with-coverage --cover-package src.lambda_function --cover-erase
```
