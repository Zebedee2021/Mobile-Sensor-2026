' Sensor Logger 托盘程序启动器
' 隐藏命令行窗口，只在系统托盘显示

Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' 获取脚本所在目录
strPath = FSO.GetParentFolderName(WScript.ScriptFullName)

' 切换到项目目录并启动托盘程序
WshShell.CurrentDirectory = strPath

' 使用 pythonw.exe 隐藏控制台窗口（如果没有 pythonw，则使用 python）
pythonExe = "pythonw"
If Not CheckCommand(pythonExe) Then
    pythonExe = "python"
End If

' 启动托盘程序（隐藏窗口）
WshShell.Run pythonExe & " scripts\tray.py", 0, False

' 检查命令是否存在
Function CheckCommand(cmd)
    On Error Resume Next
    Dim tempFile
    tempFile = FSO.GetTempName
    WshShell.Run "cmd /c " & cmd & " --version > " & tempFile & " 2>&1", 0, True
    CheckCommand = FSO.FileExists(tempFile) And (FSO.GetFile(tempFile).Size > 0)
    If FSO.FileExists(tempFile) Then FSO.DeleteFile tempFile
    On Error GoTo 0
End Function
