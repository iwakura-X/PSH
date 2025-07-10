# PSH (Python Shell) - cross-platform shell written fully in Python for Linux/MacOS, and Windows with python 3.6+
# ACHTUNG WARNING ВНИМАНИЕ 危險 ՎՏԱՆԳ!!!
This project is in open beta test and was not intended for professional use!!!

PSH is designed for those, who are tired of boring BASH/ZSH or cmd on Windows!
## Installing & Running
```bash
git clone https://github.com/iwakura-X/PSH.git
cd PSH
pip install -r requirements.txt
python3 /core/main.py
```
## Basic commands:
just run help in the command prompt

## Structure:
* - means that this will be involved in future
- '/core/' - shell's core (all magic is here)
- '/core/commands' - commands (ls, or rm -rf /*)
- '/scripts/' - user scripts (write, run, suffer) *
- '/tests/' - shell's components tests (debug feature) *
- '/utils/' - utilities (like auth module)
- '/data/' - user data(like passwords and logins)


## Roadmap
 v0.1
  - Basic commands (like ls, or cd)
 v0.2
  - Full refactoring(from one 200+ lines file, to this)
  - Aleph text editor
 v0.3(planned)
  - Scripts support
  - More colors
  - Commands history
  - Logging
  - Error handling
  - And much more!!!
