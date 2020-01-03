::@echo off
echo Run autopep8 on two levels of tree

call :autopep
for /d %%d in (*.*) do call :do1level %%d
pause
goto :eof

:do1level
pushd %1
call :autopep
for /d %%d in (*.*) do call :do2ndlevel %%d
popd
goto :eof

:do2ndlevel
cd %1
call :autopep
cd..
goto :eof

:autopep
for %%f in (*.py) do if /i not %%f==rF2data.py autopep8 -i -a -a -a %%f
