<h2>Reversi.AI</h2>

Play Reversi against your friends or against different types of AI!

<h3>How to run app</h3>
<ul>
<li>
Navigate into Reversi folder
</li>
<li>
Run
<pre>
<code>Python gui.py</code></pre>
</li>
</ul>

<h3>Help</h3>
<ul>
<li>
<b>Grey circles:</b> Possible places you can place a piece</li>
<li>
<b>Arrows: </b> Found under the board, they tell you whose turn it is
</li>
</ul>

<h3>Multiplayer:</h3> 
Click multiplayer to play with another player locally on your computer

<h3>Offline:</h3> 
Vary levels of AI difficulty by clicking "Offline 1 Player" and using the slider
<ul>
<li>Play with varying depths of Minimax AI</li>
<br>
<li>Play with varying number of simulations of Monte Carlo Tree Search AI</li>
</ul>

<h3>Online</h3>
<ol>
<li>Uncomment out line 22 of main.py 
<pre>
<code>self.net = Network()
</code></pre>
</li>
<li>Uncomment out lines 449-451 of gui.py(
<pre><code>app.network = True
app.player1.network = True
app.player2.network = True
</code></pre>
</li>
<li>
Run server.py
</li>
<li>
Run gui.py on seperate computers</li>
</ol>



<h3>Requirements</h3>
Requirements can be found in requirements.txt
<ul>
<li>
Install CMU 112-Graphics from https://www.cs.cmu.edu/~112/index.html
</li>
<li>
<b>Download Sockets:</b> run <span>"pip install sockets"</span>
</li>
<li>
<b>Download Thread6:</b> run "pip install thread6"
</li>
<li>
<b>Download Threaded:</b> run "pip install threaded"
</li>
</ul>

