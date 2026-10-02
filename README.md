
# BLREdit
Blacklight Revive Loadout Editor

# Features
<details>
  <summary>Multiple Profiles.</summary>
  <img src="/Screenshots/Readme/ProfileList.png"/>
</details>
<details>
  <summary>Camo Selection</summary>
  <img src="/Screenshots/Readme/CamoSelection.png"/>
</details>
<details>
  <summary>Stat Sorting With Highlighting</summary>
  <img src="/Screenshots/Readme/ItemListWithSorting.png"/>
</details>
<details>
  <summary>Scope Selection and Preview</summary>
  <img src="/Screenshots/Readme/Scope%20Selection.png"/>
  <img src="/Screenshots/Readme/ScopePreview.png"/>
</details>
<details>
  <summary>Weapon Tag Selection</summary>
  <img src="/Screenshots/Readme/WeaponTagSelection.png"/>
</details>
<details>
  <summary>Tactical Gear Selection</summary>
  <img src="/Screenshots/Readme/TacticalGearSelection.png"/>
</details>
<details>
  <summary>Avatar Selection</summary>
  <img src="/Screenshots/Readme/AvatarSelection.png"/>
</details>

Export Loadout to Clipboard for MagiCow's Loadout Customization bot

# Download
[Download From Github Releases](https://github.com/HALOMAXX/BLREdit/releases)

# Offline server registry checks

Before changing `Resources/ServerList.json`, run these commands from the repository
root with Python 3 (standard library only):

```
python tools/validate_server_registry.py
python -m unittest discover -s tests -v
```

The validator checks structure, property names and types, duplicate IDs and game
endpoints, and port ranges. Omitted ports retain the application's 7777 defaults.
It reads files only: it does not resolve hosts, probe servers, or launch BLREdit.
The regression suite also preserves the explicit 7778 game and info ports from
upstream PR #137. See [implementation notes](IMPLEMENTATION_NOTES.md) for scope.
