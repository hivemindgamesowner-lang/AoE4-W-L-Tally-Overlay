import json
import time
import requests
import os
import sys
from datetime import datetime, timezone
sys.dont_write_bytecode = True  # prevent creation of __pycache__

def fetch_last_game(steam_id):
    url = f"https://aoe4world.com/api/v0/players/{steam_id}/games/last"
    print(f"[DEBUG] Fetching URL: {url}")  # ← Print the URL!
    r = requests.get(url)
    if r.status_code != 200:
        print(f"API Error: HTTP {r.status_code}")
        return None
    data = r.json()
    print(f"[DEBUG] API response: {data}")  # ← Print the actual response!
    return data



# ─── CONFIG LOADING ────────────────────────────────────────────────────────────
def load_config():
    """
    Load stream‐specific settings from config.json:
      • profile_id       – your AoE4World profile
      • interval_seconds – poll frequency
      • output_file      – where to write W/L for OBS to pick up
    """
    with open("config.json", "r") as f:
        return json.load(f)


# ─── SESSION STORAGE ───────────────────────────────────────────────────────────
def save_session(session_data):
    """
    Persist session state in session.json.
    session_data is a dict holding:
      • starting_wins    – total wins on reset
      • starting_losses  – total losses on reset
      • manual_wins      – +W adjustments via button
      • manual_losses    – +L adjustments via button
      • start_time       – UNIX ts at reset
    """
    with open("session.json", "w") as f:
        json.dump(session_data, f)


def load_session():
    if os.path.exists("session.json"):
        data = json.load(open("session.json"))
    else:
        data = {
            "starting_wins":    0,
            "starting_losses":  0,
            "manual_wins":      0,
            "manual_losses":    0,
            "start_time":       time.time(),
            "last_game_id":     None
        }
        save_session(data)
    data.setdefault("manual_wins",   0)
    data.setdefault("manual_losses", 0)
    data.setdefault("last_game_id", None)
    return data





# ─── OVERLAY OUTPUT ────────────────────────────────────────────────────────────
def write_output(wins, losses, output_file):
    """
    Write the final tally to win_loss.txt (or whatever you named it).
    OBS will read this file and show:
      W : wins
      L : losses
    """
    with open(output_file, "w") as f:
        f.write(f"W : {wins}\nL : {losses}")
    print(f"[Updated] W:{wins} L:{losses}")


# ─── RESET HANDLER ──────────────────────────────────────────────────────────────
def reset_session():
    """
    True hard reset:
      • starting_wins   ← 0
      • starting_losses ← 0
      • manual_wins     ← 0
      • manual_losses   ← 0
      • start_time      ← now
      • last_game_id    ← None
    Overlay shows 0:0.
    """
    cfg = load_config()
    out = cfg["output_file"]

    session_data = {
        "starting_wins":    0,
        "starting_losses":  0,
        "manual_wins":      0,
        "manual_losses":    0,
        "start_time":       time.time(),
        "last_game_id":     None
    }
    save_session(session_data)
    write_output(0, 0, out)
    print("[Session hard reset → 0:0, counting only NEW games after this time]")

# ─── MAIN LOOP ─────────────────────────────────────────────────────────────────

def run_loop():
    cfg = load_config()
    steam_id = cfg["steam_id"]
    interval = cfg["interval_seconds"]
    out_file = cfg["output_file"]

    session = load_session()

    print("[Started polling for latest game] Press Ctrl+C to stop.")
    try:
        while True:
            session = load_session()
            url = f"https://aoe4world.com/api/v0/players/{steam_id}/games/last"
            print(f"[DEBUG] Fetching URL: {url}")
            last_game = fetch_last_game(steam_id)
            print(f"[DEBUG] last_game object: {last_game}")

            session_start_ts = session['start_time']                       # 🔑
            session_start_str = datetime.fromtimestamp(session_start_ts, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')  # 🔑
            print(f"[DEBUG] session['start_time']: {session_start_ts} ({session_start_str})")  # 🔑

            print(f"[DEBUG] session['last_game_id']: {session.get('last_game_id')}")

            if last_game and isinstance(last_game, dict) and "game_id" in last_game:
                last_game_id = last_game.get("game_id")
                updated_at = last_game.get("updated_at")
                print(f"[DEBUG] last_game_id: {last_game_id}, updated_at: {updated_at}")

                if not updated_at:
                    print("[WARNING] No 'updated_at' field in last_game. Skipping this poll.")
                    time.sleep(interval)
                    continue

                try:
                    game_ended_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00")).timestamp()
                    game_ended_str = datetime.fromisoformat(updated_at.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S UTC')
                    print(f"[DEBUG] game_ended_at: {game_ended_at} ({updated_at}) ({game_ended_str})")  # 🔑
                except Exception as e:
                    print(f"[ERROR] Failed to parse updated_at: {updated_at} ({e})")
                    time.sleep(interval)
                    continue


                if game_ended_at > session["start_time"]:
                    print(f"[DEBUG] Game ended after session start.")
                    if last_game_id != session.get("last_game_id"):
                        print(f"[DEBUG] game_id is new, not yet counted.")
                        #! Do NOT update last_game_id here yet!

                        # Find your player slot
                        slot = None
                        for team in last_game.get("teams", []):
                            for p in team:
                                print(f"[DEBUG] Checking player: {p['profile_id']} (result: {p.get('result')})")
                                if str(p["profile_id"]) == str(cfg["profile_id"]):
                                    slot = p
                                    break
                            if slot:
                                break

                        print(f"[DEBUG] slot found: {slot}")
                        if slot:
                            print(f"[DEBUG] slot result: {slot.get('result')}")
                            result = slot.get("result")
                            if result == "win":
                                session["starting_wins"] += 1
                                session["last_game_id"] = last_game_id  #! Only update here
                                print("[New Win detected]")
                                save_session(session)
                            elif result == "loss":
                                session["starting_losses"] += 1
                                session["last_game_id"] = last_game_id  #! Only update here
                                print("[New Loss detected]")
                                save_session(session)
                            else:
                                print("[DEBUG] Game in progress or result not available. Will retry on next poll.")
                        else:
                            print("[DEBUG] No matching player found in teams for your profile_id!")
                    else:
                        print(f"[DEBUG] game_id {last_game_id} already counted as last_game_id")
                else:
                    print(f"[DEBUG] Game ended at {game_ended_at}, which is before or equal to session start {session['start_time']}")

                # Write combined results to overlay file
                total_wins = session["starting_wins"] + session["manual_wins"]
                total_losses = session["starting_losses"] + session["manual_losses"]
                write_output(total_wins, total_losses, out_file)
            else:
                print("[No valid game data fetched, API error, or no games found]")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[Stopped by user]")
        sys.exit()

# ─── ENTRYPOINT ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    cfg = load_config()
    pid = cfg["profile_id"]
    out = cfg["output_file"]

    if args and args[0] == "reset":
        # Reset on‐demand via bat/script/button
        reset_session()

    elif args and args[0] == "win+":
        sess = load_session()
        sess["manual_wins"] += 1
        save_session(sess)
        total_wins = sess["starting_wins"] + sess["manual_wins"]
        total_losses = sess["starting_losses"] + sess["manual_losses"]
        write_output(total_wins, total_losses, out)
        print("[Manual] Win count +1")

    elif args and args[0] == "win-":
        sess = load_session()
        sess["manual_wins"] = max(0, sess["manual_wins"] - 1)
        save_session(sess)
        total_wins = sess["starting_wins"] + sess["manual_wins"]
        total_losses = sess["starting_losses"] + sess["manual_losses"]
        write_output(total_wins, total_losses, out)
        print("[Manual] Win count -1")

    elif args and args[0] == "loss+":
        sess = load_session()
        sess["manual_losses"] += 1
        save_session(sess)
        total_wins = sess["starting_wins"] + sess["manual_wins"]
        total_losses = sess["starting_losses"] + sess["manual_losses"]
        write_output(total_wins, total_losses, out)
        print("[Manual] Loss count +1")

    elif args and args[0] == "loss-":
        sess = load_session()
        sess["manual_losses"] = max(0, sess["manual_losses"] - 1)
        save_session(sess)
        total_wins = sess["starting_wins"] + sess["manual_wins"]
        total_losses = sess["starting_losses"] + sess["manual_losses"]
        write_output(total_wins, total_losses, out)
        print("[Manual] Loss count -1")

    else:
        # No args → start polling loop
        run_loop()

