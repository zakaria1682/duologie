
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
  <li>a: Algorithm. Hier hoort de naam van de file met daarin het gewenste algoritme om getest te worden</li>
  <li>n: Netlist. Hier hoort het nummer van de netlist waar het algoritme op getest moet worden.
         test_runs.py bepaalt automatisch welke chip-print hierbij hoort.</li>
  <li>tt: Total Time: Hier hoort de totale tijd waarin het algoritme herhaaldelijk uitgevoert moet worden.</li>
  <li>tpr: Time Per Run: Hier hoort de maximale tijd die elke uitvoer van het algoritme heeft om tot één oplossing te komen</li>
</ol>