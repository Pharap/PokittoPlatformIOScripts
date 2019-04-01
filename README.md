# Pokitto PlatformIO Scripts

A collection of useful scripts for a PlatformIO environment building for Pokitto

## `pokitto_update_ld.py`

Updates the Pokitto's `.ld` file, won't prevent compilation if updating fails and offers the option of disabling updating by specifying `disable_ld_auto_update` in the `platformio.ini`

## `pokitto_copy_bin.py`

Copies the `.bin` file from the `/.pioenvs/pokitto` folder to the project folder.
