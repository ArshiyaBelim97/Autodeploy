
provider "aws" { region = "us-east-1" }

resource "aws_lambda_function" "app" {
  function_name = "a90e16f7-lambda"
  handler = "lambda_handler.handler"
  runtime = "python3.11"
  role = "arn:aws:iam::123456789:role/demo-role"
  filename = "s3://autodeploy-lambda-artifacts-a90e16f7/a90e16f7_lambda.zip"
}

resource "aws_apigatewayv2_api" "api" {
  name = "a90e16f7-api"
  protocol_type = "HTTP"
}
