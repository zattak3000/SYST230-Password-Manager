# SYST 230 Password Manager Project
## Group 4
### Developers
* Anosh Mian
* Rohan Puvvada
* John Schultz-Kovach
* Zack Wagner

## Default File Behavior
By default this program searches for `vault.bin` in the current directory and will select it if found. If no such file is found, the user must create a new file which can be any name. But, the program will still only automatically select any file named `vault.bin` in the current directory, even if it was not the last file accessed.

## New File Behavior
If a new vault file is created, any password may be entered on the login screen. This password will become the one used to open the file in the future.