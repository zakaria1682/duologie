
# Chips & Circuits 

The assignment is to implement all nets in all netlists at minimum cost.
A few steps to pave the way towards a program:

<ol>
  <li>Build a computer program that holds a data structure for a grid with fixed gates.</li>
  <li>Expand your program by making a data structure for a netlist. Make sure it holds a few nets, and that the program has a cost function to calculate the total wire length.</li>
  <li>Add 7 more layers by stacking them on top of the base layer. Try to get as many as possible of the nets in. You can either build up wire-by-wire, or remove collisions one by one. Do not worry if you can not fit all of them initially; it is still possible to measure performance by the percentage of nets that you have been able to fit in with a specific algorithm.</li>
  <li>Try to get all the nets in with minimal costs. Record all your results, so you can present them later.</li>
</ol>

## Instructies voor het gebruik van test_runs (het ophalen van de resultaten)

Door middel van test_runs.py kunnen de gemaakte algoritmes worden aangeroepen.
Bij het aanroepen worden een aantal argumenten gevraagd die de uitkomst van de runs beïnvloeden.
De argumenten zijn als volgt gestructureerd:

<p style="font-family:arial">python3 test_runs.py a n tt tpr<p>
waarbij:
<ol>
  <li><b>a</b>: Algorithm. Hier hoort de naam van de file met daarin het gewenste algoritme om getest te worden<br>
         De opties in dit geval zijn: random_solve.py, BFS.py & a_star.py
         </li>
  <li><b>n</b>: Netlist. Hier hoort het nummer van de netlist waar het algoritme op getest moet worden.
         test_runs.py bepaalt automatisch welke chip-print hierbij hoort.<br>
         Hier kan worden gekozen voor een getal (int) tussen 1 & 9
         </li>
  <li><b>tt</b>: Total Time: Hier hoort de totale tijd waarin het algoritme herhaaldelijk uitgevoert moet worden.
                 (in aantal seconden in ints)</li>
  <li><b>tpr</b>: Time Per Run: Hier hoort de maximale tijd die elke uitvoer van het algoritme heeft om tot één 
                  oplossing te komen (in aantal seconden in ints)</li>
</ol>

Na het aanroepen van test_runs.py op deze manier zal het gegeven algoritme worden uitgevoerd voor tt seconden.
test_runs.py roept het algoritme herhaaldelijk aan, en in het bestand van het algoritme wordt afhankelijk van
welke netlist is gegeven het algoritme één maal uitgevoerd. Hierbij wordt de tijd gemeten die nodig is voor enkel
en alleen het solven. Vervolgens worden statistieken van het bord verzameld.<br>

De statistieken die worden verzameld:
<ul>
  <li>Excecution time per run</li>
  <li>Hoeveelheid afgemaakte nets versus totale aantal nets</li>
  <li>Cost van oplossing</li>
</ul>

Daarnaast wordt ook het beste geval van elk van deze statistieken verzameld,
en de best gevonden oplossing (rekening houdend met elk van deze statistieken).<br>

Elke individuele run van het algoritme zal worden aangekondigd door het printen van "run: " gevolgd door
het nummer van de huidige run, en voor elke afgemaakte run zullen de bijbehorende statistieken per run
op een nieuwe regel worden afgeschreven in output/output.csv.
Enkele gemiddelden en de beste statistieken worden ook nog uitgeschreven naar
stdout.

