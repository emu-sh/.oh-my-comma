# Commands

#### `emu fork`:
🍴 Manage installed forks, or install a new one
- `emu fork switch`: 🍴 Switch between any openpilot fork
  - Arguments 💢:
    - username: 👤 The username of the fork's owner to install
    - branch (optional): 🌿 Branch to switch to, will use default branch if not provided
  - Example 📚:
    - `emu fork switch stock devel`
- `emu fork list`: 📜 See a list of installed forks and branches
  - Arguments 💢:
    - fork (optional): 🌿 See branches of specified fork
  - Example 📚:
    - `emu fork list stock`

#### `emu panda`:
🐼 panda interfacing tools
- `emu panda flash`: 🐼 flashes panda with make recover (usually works with the C2)
- `emu panda flash2`: 🎍 flashes panda using Panda module (usually works with the EON)

#### `emu debug`:
de-🐛-ing tools
- `emu debug controlsd`: logs controlsd to /data/output.log by default
  - Arguments 💢:
    - -o, --output: Name of file to save log to
  - Example 📚:
    - `emu debug controlsd /data/controlsd_log`

#### `emu device`:
📈 Statistics about your device
- `emu device battery`: 🔋 see information about the state of your battery
- `emu device reboot`: ⚡ safely reboot your device
- `emu device shutdown`: 🔌 safely shutdown your device
