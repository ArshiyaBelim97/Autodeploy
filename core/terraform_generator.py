from pathlib import Path

def generate_terraform_for_run(tf_dir, meta):
    tf_main = tf_dir/"main.tf"
    tf_main.write_text(f'''
provider "aws" {{ region = "{meta['region']}" }}

resource "aws_lambda_function" "app" {{
  function_name = "{meta['run_id']}-lambda"
  handler = "lambda_handler.handler"
  runtime = "python3.11"
  role = "arn:aws:iam::123456789:role/demo-role"
  filename = "s3://{meta['artifact_s3_bucket']}/{meta['artifact_s3_key']}"
}}

resource "aws_apigatewayv2_api" "api" {{
  name = "{meta['run_id']}-api"
  protocol_type = "HTTP"
}}
''')
