from pathlib import Path
import zipfile, shutil, os

def package_for_lambda(src_dir: Path, meta: dict, run_dir: Path):
    package_dir = run_dir/"package"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    reqs = meta.get("requirements", [])
    if "awsgi" not in [r.split("==")[0] for r in reqs]:
        reqs.append("awsgi")

    tmp_reqs = run_dir/"tmp_requirements.txt"
    tmp_reqs.write_text("\n".join(reqs))
    os.system(f"python -m pip install -r {tmp_reqs} -t {package_dir}")

    for item in src_dir.iterdir():
        dest = package_dir/item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    handler_py = package_dir/"lambda_handler.py"
    if "flask_file" in meta:
        flask_mod = meta["flask_file"].replace(".py","").replace("/",".")
        handler_py.write_text(f"""
import awsgi
from {flask_mod} import {meta.get('flask_app_var','app')} as flask_app

def handler(event, context):
    return awsgi.response(flask_app, event, context)
""")
    else:
        handler_py.write_text("def handler(event, context): return {'statusCode':200,'body':'Hello'}")

    artifact = run_dir/f"{meta['run_id']}_lambda.zip"
    with zipfile.ZipFile(artifact, "w", zipfile.ZIP_DEFLATED) as z:
        for f in package_dir.rglob("*"):
            z.write(f, f.relative_to(package_dir))
    return artifact
