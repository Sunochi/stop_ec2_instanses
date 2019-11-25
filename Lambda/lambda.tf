variable "iam_role_prefix" {
  default = "lambda_"
}
variable "lambda_function_name" {}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "./workspace"
  output_path = "./lambda.zip"
}

data "aws_iam_role" "lambda_role" {
  name = "${format("%s%s", var.iam_role_prefix, var.lambda_function_name)}"

}

resource "aws_lambda_function" "lambda_function" {
  filename         = "${data.archive_file.lambda_zip.output_path}"
  function_name    = "${var.lambda_function_name}"
  role             = "${data.aws_iam_role.lambda_role.arn}"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
  runtime          = "python3.7"
  timeout          = 300
  environment {
    variables = {
      TZ = "Asia/Tokyo"
    }
  }
}
