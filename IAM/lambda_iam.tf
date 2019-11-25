variable "iam_role_prefix" {
  default = "lambda_"
}
variable "lambda_function_name" {
}

data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "${format("%s%s", var.iam_role_prefix, var.lambda_function_name)}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

data "aws_iam_policy_document" "EC2_instance_stop_policy" {
  statement {
    actions = [
      "ec2:DescribeInstances",
      "ec2:DescribeRegions",
      "ec2:DescribeTags",
      "ec2:StopInstances"
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "EC2_instance_stop_policy" {
  name   = "EC2InstanceStop"
  role   = "${aws_iam_role.lambda_role.name}"
  policy = "${data.aws_iam_policy_document.EC2_instance_stop_policy.json}"
}

locals {
  enhancedpolices = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
  ]
}

resource "aws_iam_role_policy_attachment" "lambda_role" {
  count      = length(local.enhancedpolices)
  role       = aws_iam_role.lambda_role.name
  policy_arn = element(local.enhancedpolices, count.index)
}

