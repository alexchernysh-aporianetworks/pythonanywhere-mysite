#!/usr/bin/env python3
import os, sys, time, signal, django

sys.path.append('/home/Karmel/mysite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mysite.models import ScriptTask

def is_pgid_alive(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True

def kill_group(pgid: int) -> (bool, str):
    # SIGINT -> SIGTERM -> SIGKILL, verify PGID is gone
    for sig, wait_s in [(signal.SIGINT, 2.0), (signal.SIGTERM, 2.0), (signal.SIGKILL, 1.5)]:
        try:
            os.killpg(pgid, sig)
        except ProcessLookupError:
            return True, f"PGID {pgid} already gone."
        except Exception as e:
            return False, f"Failed sending {sig} to PGID {pgid}: {e}"

        end = time.time() + wait_s
        while time.time() < end:
            if not is_pgid_alive(pgid):
                return True, f"Killed PGID {pgid} with {sig}."
            time.sleep(0.2)

    if is_pgid_alive(pgid):
        return False, f"PGID {pgid} still alive after SIGKILL."
    return True, f"PGID {pgid} gone."

def parse_pgid_from_output(output: str):
    pgid = None
    for line in (output or "").splitlines()[:15]:
        if line.startswith("CHILD_PGID:"):
            v = line.split(":", 1)[1].strip()
            if v.isdigit(): return int(v)
        if line.startswith("PGID:"):
            v = line.split(":", 1)[1].strip()
            if v.isdigit(): pgid = int(v)
    return pgid

def main():
    print("killer_daemon started", flush=True)
    while True:
        # לקחת כמה משימות בכל סיבוב כדי לא להעמיס
        tasks = ScriptTask.objects.filter(status="STOP_REQ")[:20]
        for t in tasks:
            pgid = parse_pgid_from_output(t.output)
            if not pgid:
                t.status = "FAILED"
                t.error = "STOP_REQ but no PGID found in output."
                t.save()
                continue

            ok, msg = kill_group(pgid)

            if ok:
                t.status = "KILLED"
                t.error = None
                t.output = (t.output or "") + f"\n✅ killer_daemon: {msg}"
            else:
                # לא משקרים — נשאיר STOP_REQUESTED כדי שינסה שוב,
                # או אפשר לשנות ל-KILL_FAILED אם יש אצלך סטטוס כזה.
                t.error = msg
                t.output = (t.output or "") + f"\n❌ killer_daemon: {msg}"
            t.save()

        time.sleep(1.0)

if __name__ == "__main__":
    main()
