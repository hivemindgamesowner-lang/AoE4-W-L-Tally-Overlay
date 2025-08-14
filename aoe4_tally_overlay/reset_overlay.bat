@echo off
cd /d %~dp0
PowerShell -WindowStyle Hidden -Command "Start-Process '..\\python.exe' -ArgumentList 'main.py reset' -WorkingDirectory '%~dp0'-WindowStyle Hidden"


def reset_session():
    config = load_config()
    profile_id = config["profile_id"]
    output_file = config["output_file"]

    current_wins, current_losses = fetch_stats(profile_id)
    if current_wins is not None:
        save_session(current_wins, current_losses)
        write_output(0, 0, output_file)  # Immediately show 0/0 in overlay
        print("[Session reset to current stats and overlay set to 0/0]")
