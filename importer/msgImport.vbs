Option Explicit

Dim strFile, objFSO, strConnect, strOutputFile, rs, objConn, url, interval, nbrOfMsgPerInterval

' set loop interval
interval = 5000
nbrOfMsgPerInterval = 5
' Access database
strFile = "data.mdb"
' File to store last id
strOutputFile = "lastcheck.out"

' Url to send messages to, notes:
' >>>	1. make sure the url is a trusted site in internet options
' >>>	2. make sure in custom levels: "miscellaneous/access data sources across domains" is enabled
url = "http://tweetwall.yppy.eu"
dim pwd:pwd="6d9cec07aaa15b417c1698f7a2642e0e6"

' Check if the specified database file exists
WScript.Echo "Check if database file exists: " + strFile
Set objFSO = CreateObject( "Scripting.FileSystemObject" )
If Not objFSO.FileExists( strFile ) Then 
	WScript.Echo "File does not exists, please check the file location"
	WScript.Quit 1
Else
	WScript.Echo "Database file found"
End if
Set objFSO = Nothing

' ############## Get last id from disk if exists ###################
Dim lastIdFromdisk: lastIdFromDisk = "0"
Set objFSO = CreateObject("Scripting.FileSystemObject")
If objFSO.FileExists( strOutputFile ) then
	dim objFile: Set objFile = objFSO.OpenTextFile(strOutputFile, 1)
	lastIdFromdisk = objFile.Readline
	WScript.Echo "Read the last id from disk: " + lastIdFromdisk
	If not IsNumeric(lastIdFromdisk) then
		WScript.Echo "not nummeric, so resetting to 0"
		lasIdFromdisk = "0"
	End if
	objFile.Close
Else
	WScript.Echo "First run, there is no file with lastid yet"
End If
' ##################################################################

while true
	WScript.Echo "Checking for next "+cstr(nbrOfMsgPerInterval)+" messages"
	
	' Connect to the MS-Access database ################################
	Set objConn = CreateObject( "ADODB.Connection" )
	Set rs = CreateObject("ADODB.Recordset")
	strConnect = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" & strFile
	objConn.Open strConnect
	rs.Open "SELECT top "+cstr(nbrOfMsgPerInterval)+" ID, MessageText, MessageOrigin FROM Data WHERE ID > "+lastIdFromdisk+" ORDER BY ID ASC" , objConn, 3, 3

	dim msg, origin
	while not rs.eof
	
		lastIdFromdisk = CStr(rs.fields(0))
		msg    		   = rs.fields(1)
		origin   	   = rs.fields(2)
			
		If Len(msg) > 0 Then	
			msg = URLEncode(msg)
			origin = URLEncode(origin)
			WScript.Echo "From: " + origin + " Message: " +msg
			
			Dim o, tweetUrl
			Set o = CreateObject("MSXML2.XMLHTTP.3.0")
			tweetUrl = url + "/tweet?username=" + origin + "&message=" + msg
			o.open "GET", tweetUrl, False, "feeder", pwd
			
			WScript.Echo "Requesting url: " + tweetUrl
			o.send
			WScript.Echo "Response: " + o.responseText
			
			If o.status <> 200 Then
				WScript.Echo "Error status: " + cstr(o.status)
				WScript.Quit 1
			End If
		Else
			WScript.Echo "Message is empty, so skipping..."
		End If
	rs.movenext
	wend

	' close all db objects
	rs.Close
	objConn.Close

	' write lastIdFromdisk to disk ############################################
	Dim objFileSystem, objOutputFile
	Set objFileSystem = CreateObject("Scripting.fileSystemObject")
	Set objOutputFile = objFileSystem.CreateTextFile(strOutputFile, TRUE)
	objOutputFile.WriteLine(lastIdFromdisk)
	objOutputFile.Close
	Set objFileSystem = Nothing
	
	WScript.Sleep interval
wend

' convert a string so that it can be used on a URL query string
Public Function URLEncode(sRawURL)
    Dim iLoop 
    Dim sRtn 
    Dim sTmp
    Const sValidChars = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:/.?=_-$(){}~&"

    If Len(sRawURL) > 0 Then
        ' Loop through each char
        For iLoop = 1 To Len(sRawURL)
            sTmp = Mid(sRawURL, iLoop, 1)

            If InStr(1, sValidChars, sTmp, vbBinaryCompare) = 0 Then
                ' If not ValidChar, convert to HEX and p
                '     refix with %
                sTmp = Hex(Asc(sTmp))

                If sTmp = "20" Then
                    sTmp = "+"
                ElseIf Len(sTmp) = 1 Then
                    sTmp = "%0" & sTmp
                Else
                    sTmp = "%" & sTmp
                End If
            End If
            sRtn = sRtn & sTmp
        Next
        URLEncode = sRtn
	else 
		URLEncode = ""
    End If
End Function