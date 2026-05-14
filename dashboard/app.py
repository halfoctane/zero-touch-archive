from flask import Flask, render_template, jsonify
import os, glob, datetime, pytz

IST = pytz.timezone("Asia/Kolkata")

app = Flask(__name__)
ARCHIVES_DIR = "/archives"

def get_backups():
    files = glob.glob(os.path.join(ARCHIVES_DIR, "*.sql*"))
    backups = []
    for f in sorted(files, reverse=True):
        stat = os.stat(f)
        size = stat.st_size
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime, tz=pytz.utc).astimezone(IST)
        backups.append({
            "filename": os.path.basename(f),
            "size_bytes": size,
            "size_display": f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB",
            "time": mtime.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "ok" if size > 100 else "fail"
        })
    return backups

@app.route("/")
def index():
    backups = get_backups()
    total = len(backups)
    ok = sum(1 for b in backups if b["status"] == "ok")
    last = backups[0] if backups else None
    total_size = sum(b["size_bytes"] for b in backups)
    total_size_display = f"{total_size/1024/1024:.1f} MB" if total_size > 1024*1024 else f"{total_size/1024:.1f} KB"
    success_rate = f"{int(ok/total*100)}%" if total > 0 else "N/A"
    return render_template("index.html",
        backups=backups, total=total, ok=ok,
        last=last, total_size=total_size_display,
        success_rate=success_rate,
        healthy=(ok == total and total > 0)
    )

@app.route("/api/backups")
def api_backups():
    return jsonify(get_backups())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)