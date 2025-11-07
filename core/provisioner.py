def run_terraform_apply(tf_dir):
    print(f"Running terraform apply in {tf_dir}... (mock)")
    return {"api_url": f"https://mock-api-{tf_dir.name}.execute-api.mock-region.amazonaws.com/"}

def healthcheck_url(url):
    print(f"Checking health at {url}... (mock)")
    return True, {"message":"Hello from AI Autodeploy!"}
