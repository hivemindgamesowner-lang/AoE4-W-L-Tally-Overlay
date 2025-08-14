# adjust_session.py
import sys, json
from main import load_session, save_session, load_config, write_output

def adjust(action):
    cfg         = load_config()
    pid         = cfg["profile_id"]
    out_file    = cfg["output_file"]

    session     = load_session()

    if action == "win+":
        session["manual_wins"]   += 1
    elif action == "win-":
        session["manual_wins"]   = max(0, session["manual_wins"]   - 1)
    elif action == "loss+":
        session["manual_losses"] += 1
    elif action == "loss-":
        session["manual_losses"] = max(0, session["manual_losses"] - 1)
    else:
        print("Unknown action.")
        return

    save_session(session)
    # immediately refresh overlay using local session values only!
    total_wins = session["starting_wins"] + session["manual_wins"]
    total_losses = session["starting_losses"] + session["manual_losses"]
    write_output(total_wins, total_losses, out_file)
    print(f"[Manual] {action} applied – manual_wins={session['manual_wins']}, manual_losses={session['manual_losses']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python adjust_session.py <win+|win-|loss+|loss->")
    else:
        adjust(sys.argv[1])
