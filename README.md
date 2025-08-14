===============================
AoE4 Overlay Tally - Instructions
===============================

This tool automatically tracks your wins and losses in Age of Empires IV for overlay display, 
with easy manual adjustment and hotkey/stream deck support.

[**⬇ Download Portable Build (Latest Release)**](https://github.com/hivemindgamesowner-lang/AoE4-W-L-Tally-Overlay/releases/download/v1.0.0/aoe_tally.zip)


![Overlay demo](demo.gif)

--------------------------------
Setup
--------------------------------

1. Configure Your Steam and Player IDs:

   - Open 'config.json' in Notepad (or any text editor).
   - Update the following fields:
        "steam_id": "YOUR_STEAM_ID_HERE"
        "profile_id": YOUR_AOE4WORLD_PROFILE_ID_HERE

     - You can find your profile ID at the end of your AoE4World URL:
       Example: https://aoe4world.com/players/12345678
                -> profile_id is 12345678

   - Save the file when done.

--------------------------------
Basic Usage
--------------------------------

- To start the overlay:
    Double-click 'run_overlay.bat'
    (or 'start_debug.bat' for detailed logs)

- To stop the overlay:
    Double-click 'stop_overlay.bat' or close the command window.

--------------------------------
Manual Controls (Batch Files)
--------------------------------

The following batch files allow you to manually adjust your tally at any time:

- win_plus.bat      → Add 1 win
- win_minus.bat     → Remove 1 win
- loss_plus.bat     → Add 1 loss
- loss_minus.bat    → Remove 1 loss
- reset_overlay.bat → Reset the session and counters to 0

You can create shortcuts to these files and place them on your Desktop or assign them to Stream Deck keys for one-tap control!

--------------------------------
How the Overlay Works
--------------------------------

- Your current wins/losses are always output to 'win_loss.txt'
- Add a text source in OBS (or your streaming software) that points to this file to display your tally live.

--------------------------------
Support & Troubleshooting
--------------------------------

- If you need help, contact FletcherTime on Twitch:
    https://www.twitch.tv/fletchertime
  or on Discord.

- Make sure to restart the overlay after changing your Steam or profile IDs.

- If your manual changes don't update instantly, make sure the overlay is running.

--------------------------------
Enjoy your matches!
GLHF,
FletcherTime
===============================
