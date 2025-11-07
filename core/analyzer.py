from pathlib import Path
import re

def analyze_repo(src_dir):
    src_dir = Path(src_dir)
    meta = {}
    if (src_dir/"requirements.txt").exists() or any(p.suffix==".py" for p in src_dir.rglob("*.py")):
        meta["app_type"] = "python"
        py_files = list(src_dir.rglob("*.py"))
        for p in py_files:
            txt = p.read_text(errors="ignore")
            if "Flask" in txt:
                meta["flask_file"] = str(p.relative_to(src_dir))
                m = re.search(r"(\w+)\s*=\s*Flask", txt)
                meta["flask_app_var"] = m.group(1) if m else "app"
                break
        meta.setdefault("handler_module", meta.get("flask_file","app.py").replace(".py",""))
        meta.setdefault("handler_name", "handler")
        deps = (src_dir/"requirements.txt").read_text().splitlines() if (src_dir/"requirements.txt").exists() else []
        meta["requirements"] = [d.strip() for d in deps if d.strip()]
    else:
        meta["app_type"] = "unknown"
    return meta
