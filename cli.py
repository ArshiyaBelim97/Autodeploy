import os
import subprocess
import zipfile
import boto3
import tempfile
import typer
from botocore.exceptions import ClientError

app = typer.Typer()

@app.command()
def deploy(
    git_url: str = typer.Option(..., help="GitHub repository URL"),
    region: str = typer.Option("us-east-1", help="AWS region"),
    s3_bucket: str = typer.Option("auto-deploy-artifacts", help="S3 bucket name for deployment artifact"),
):
    typer.echo("🚀 Starting AutoDeployment process...")

    session = boto3.Session(region_name=region)
    s3_client = session.client("s3")
    lambda_client = session.client("lambda")
    api_client = session.client("apigatewayv2")

    # Step 1: Clone repo
    temp_dir = tempfile.mkdtemp()
    typer.echo(f"📦 Cloning repository: {git_url}")
    subprocess.run(["git", "clone", git_url, temp_dir], check=True)

    # Step 2: Zip repository
    zip_path = os.path.join(temp_dir, "app.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    zf.write(file_path, os.path.relpath(file_path, temp_dir))

    # Step 3: Create S3 bucket (if not exists)
    try:
        s3_client.head_bucket(Bucket=s3_bucket)
        typer.echo(f"🪣 S3 bucket '{s3_bucket}' already exists.")
    except ClientError:
        typer.echo(f"🪣 Creating S3 bucket '{s3_bucket}'...")
        s3_client.create_bucket(
            Bucket=s3_bucket,
            CreateBucketConfiguration={"LocationConstraint": region},
        )

    # Step 4: Upload zip
    s3_key = os.path.basename(zip_path)
    s3_client.upload_file(zip_path, s3_bucket, s3_key)
    typer.echo(f"✅ Uploaded ZIP to S3: s3://{s3_bucket}/{s3_key}")

    # Step 5: Create Lambda function
    function_name = "autoDeployLambda"
    role_arn = "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE"  # Replace later or automate IAM

    with open(zip_path, "rb") as f:
        zipped_code = f.read()

    try:
        typer.echo("🧠 Creating Lambda function...")
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python3.9",
            Role=role_arn,
            Handler="lambda_function.handler",
            Code={"ZipFile": zipped_code},
            Timeout=30,
            MemorySize=128,
            Publish=True,
        )
        typer.echo("✅ Lambda created.")
    except lambda_client.exceptions.ResourceConflictException:
        typer.echo("♻️ Lambda already exists. Updating code...")
        lambda_client.update_function_code(FunctionName=function_name, ZipFile=zipped_code)

    # Step 6: Create API Gateway and integrate
    typer.echo("🌐 Setting up API Gateway...")
    api = api_client.create_api(Name="AutoDeployAPI", ProtocolType="HTTP")
    api_id = api["ApiId"]

    integration = api_client.create_integration(
        ApiId=api_id,
        IntegrationType="AWS_PROXY",
        IntegrationUri=f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/arn:aws:lambda:{region}:YOUR_ACCOUNT_ID:function:{function_name}/invocations",
        PayloadFormatVersion="2.0",
    )

    api_client.create_route(
        ApiId=api_id,
        RouteKey="GET /",
        Target=f"integrations/{integration['IntegrationId']}",
    )

    api_client.create_stage(
        ApiId=api_id,
        StageName="prod",
        AutoDeploy=True,
    )

    typer.echo("🔗 Adding permission for API Gateway to invoke Lambda...")
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId="apigateway-access",
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=f"arn:aws:execute-api:{region}:YOUR_ACCOUNT_ID:{api_id}/*/*/*",
    )

    typer.echo("✅ Deployment complete!")
    typer.echo(f"🌍 Public API URL: https://{api_id}.execute-api.{region}.amazonaws.com/prod/")

if __name__ == "__main__":
    app()
