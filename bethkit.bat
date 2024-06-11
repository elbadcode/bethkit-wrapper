
powershell Start -File cmd.exe -Verb RunAs
pushd "%~dp1" 
%~dp0bethkit.exe convert "%~1" "%~n1.esx"
REN "%~n1.esx" "%~n1.xml"
start "" "%~n1.xml"
python %~dp0getEDIDs.py "%~n1.xml" "%~dp1%"
