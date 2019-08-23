echo git bash commands to load submodules
rem Automated login
git config --global credential.helper wincred

rem rmdir --ignore-fail-on-non-empty pyDirectInputKeySend
git submodule add -f https://github.com/TonyWhitley/hpp2py
