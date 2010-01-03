<%@ LANGUAGE="VBSCRIPT" %>
<HTML>
<HEAD>
<META NAME="GENERATOR" Content="Microsoft Visual InterDev 1.0">
<META HTTP-EQUIV="Content-Type" content="text/html; charset=iso-8859-1">
<TITLE>Document Title</TITLE>
</HEAD>
<BODY>

<H1 ALIGN=CENTER>Tic Tac Toe</H1>

<%
'	Variables:
'		MOVE=0-8 the position of the user's move
'		XBOARD=bitmap of X's board positions
'		OBOARD=bitmap of O's board positions
'		XCOUNT=packed counts of X's board ranks
'		OCOUNT=packed counts of O's board ranks

DIM rgMoveCount(8)
rgMoveCount(0) = 262657
rgMoveCount(1) = 4097
rgMoveCount(2) = 2129921
rgMoveCount(3) = 520
rgMoveCount(4) = 2363400
rgMoveCount(5) = 32776
rgMoveCount(6) = 2097728
rgMoveCount(7) = 4160
rgMoveCount(8) = 294976
cntInit = 2396745
cntWin = 9586980

' Add some variability to computer play by shuffling the move trial order
DIM mpmove(8)
for move = 0 to 8
	mpmove(move) = move
next

Randomize
for move = 0 to 8
	iSwap = Int(Rnd * 9)
	t = mpmove(move)
	mpmove(move) = mpmove(iSwap)
	mpmove(iSwap) = t
next

if Request.Form("XBOARD") = "" OR Request.Form("Submission") = "New Game" then
	XBOARD = 0
	OBOARD = 0
	XCOUNT = cntInit
	OCOUNT = cntInit
else
	XBOARD = Request.Form("XBOARD")
	OBOARD = Request.Form("OBOARD")
	XCOUNT = Request.Form("XCOUNT")
	OCOUNT = Request.Form("OCOUNT")
	For cell = 0 To 8
		if Request.Form("MOVE"&cell&".X") <> "" then
			MOVE = cell
			Exit For
		End If
	Next
	' Only accept the move if into an empty space and there is not
	' already a win - otherwise just ignore and return the same board position.
	If ((XBOARD AND 2^MOVE) = 0) AND _
			((OBOARD AND 2^MOVE) = 0) AND _
			((OCOUNT AND cntWin) = 0) Then
		XBOARD = XBOARD OR 2^MOVE
		XCOUNT = XCOUNT + rgMoveCount(MOVE)

		
		cmoveTest = 0

		result = BestMove(OBOARD, XBOARD, OCOUNT, XCOUNT, move)
		if move >= 0 then
			OBOARD = OBOARD OR 2^move
			OCOUNT = OCOUNT + rgMoveCount(move)
		end if

		if result = 1 AND ((OCOUNT AND cntWin) = 0) then
			Response.Write "<H2>You're gonna lose!</H2>"
		end if
	end if
end if


' Return 1 for win, 0 for draw, -1 for loss.  moveBest returns best move from this
' board position.
Function BestMove(brdMine, brdHis, cntMine, cntHis, ByRef moveBest)
	dim move
	dim iMove
	moveBest = -1
	resultBest = 0

	' Look for a single move win first of all
	for move = 0 to 8
		if ((brdMine AND 2^move) = 0) AND ((brdHis AND 2^move) = 0) AND _
				((cntMine + rgMoveCount(move)) AND cntWin) then
			cmoveTest = cmoveTest + 1
			BestMove = 1
			moveBest = move
			exit Function
		end if
	next

	for iMove = 0 to 8
		move = mpmove(iMove)
		if ((brdMine AND 2^move) = 0) AND ((brdHis AND 2^move) = 0) then
			cmoveTest = cmoveTest + 1
			result = - BestMove(brdHis, brdMine OR 2^move, _
					cntHis, cntMine + rgMoveCount(move), moveHis)
			if (moveBest = -1) OR (result > resultBest) then
				moveBest = move
				resultBest = result
				if resultBest = 1 then
					BestMove = resultBest
					exit Function
				end if
			end if
		end if 
	next
	BestMove = resultBest
End Function
%>

<FORM METHOD=POST>
<CENTER>
<TABLE BORDER=1>
<INPUT TYPE=HIDDEN NAME="XBOARD" VALUE=<%=XBOARD%>>
<INPUT TYPE=HIDDEN NAME="OBOARD" VALUE=<%=OBOARD%>>
<INPUT TYPE=HIDDEN NAME="XCOUNT" VALUE=<%=XCOUNT%>>
<INPUT TYPE=HIDDEN NAME="OCOUNT" VALUE=<%=OCOUNT%>>

<%' Draw Board
for row = 0 to 2
	Response.Write "<TR>"
	for col = 0 to 2
		cell = row*3+col
		if XBOARD AND 2^cell then
			stImage = "X.gif"
		elseif OBOARD AND 2^cell then
			stImage = "O.gif"
		else
			stImage = "Blank.gif"
		end if
		Response.Write "<TD>"
		Response.Write "<INPUT TYPE=IMAGE NAME=MOVE" & row*3+col & _
				" SRC=""images/" & stImage & """>"
	next
next
%>

</TABLE>
<p><INPUT TYPE=SUBMIT NAME=Submission VALUE="New Game">
</CENTER>
</FORM>
<% if cmoveTest <> 0 then %>
<I><%=cmoveTest%> trial moves made.</I>
<% end if %>

</BODY>
</HTML>
