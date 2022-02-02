
# Chips & Circuits 

In deze repository staat code om het Chips an Circuits probleem op te lossen. In het Chips & Circuits
probleem is het de bedoeling dat er <i>nets</i> worden gemaakt tussen <i>gates</i> op een <i>chip-print</i>.
De gegeven informatie om een probleem in het Chips & Circuits format op te kunnen lossen is:
<ul>
  <li>Een <i>print</i>, oftewel een verzameling genummerde <i>gates</i>, elk met een stel coördinaten.</li>
  <li>Een netlist: een verzameling duo's van integers, waarvan elke integer een gate voorsteld. Het duo
      representeert een connectie die gemaakt moet worden op de chip-print tussen de twee gates in het duo.</li>
</ul>

<br>

Een complete en correcte oplossing zorgt ervoor dat elke gevraagde connectie in de netlist succesvol is gemaakt
op het bord. Echter gaat Chips & Circuits verder dan alleen het vinden van een correcte oplossing. Het is ook
een optimalisatieprobleem. Elk stukje wire draagt een cost (van 1) met zich mee en het is de bedoeling om een
configuratie te vinden met een zo klein mogelijke cost.<br>
Daarnaast geldt ook dat er geen overlap mag plaatsvinden. Is er meer dan één wire aanwezig op een enkel bord-segment,
dan is de oplossing ongeldig. Intersectie, dus alleen het kruisen van nets, is wel toegestaan maar is duur. Elke
intersectie op een bord met nets verhoogd de kosten van die configuratie met 300.<br><br>
De totale cost van een bepaalde configuratie kan worden berekend met de volgende formule:<br>

<p style="font-family:arial">C = n + 300 * k<p><br>

Waar C de totale cost is, n het aantal wires en k het aantal intersecties.





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
         test_runs.py bepaalt automatisch welke chip-print hierbij hoort<br>
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

