
# Chips & Circuits 

In deze repository staat code om het Chips an Circuits probleem op te lossen. In het Chips & Circuits
probleem is het de bedoeling dat er <i>nets</i> worden gemaakt tussen <i>gates</i> op een <i>chip-print</i>.
De gegeven informatie om een probleem in het Chips & Circuits format op te kunnen lossen is:
<ul>
  <li>Een <i>print</i>, oftewel een verzameling genummerde <i>gates</i>, elk met een stel coördinaten.</li>
  <li>Een <i>netlist</i>: een verzameling duo's van integers, waarvan elke integer een gate voorsteld. Het duo
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

<p style="font-family:arial">C = n + 300 * k<p>

Waar C de totale cost is, n het aantal wires en k het aantal intersecties.




## Classes

De representatie van de case in deze repository bestaat ten eerste uit een bord: de chip-print. De dimensies van de chip-print worden bepaald door een rechthoek aan ruimte te maken waar de gegeven gates nog net in passen. Vervolgens voegen we aan deze ruimte nog één extra ring aan ruimte toe om de rechthoek heen door in de maximale x en y elk twee lengtes groter te maken. Passen de gates in een 4x5 rechthoek, dan is ons "speelveld" een rechthoek van 6x7. Daarnaast is het bord ook gelaagd, met nog zeven extra lagen bovenop de bodem. De hoeveelheid lagen is onafhankelijk van de input en is altijd acht. Dit resulteert in een 3d ruimte wat er voor zorgt dat nets ook in de hoogte kunnen uitbreiden, en dus over andere nets heen kunnen lopen om zo intersecties te voorkomen. 
<br>

Gates en hun locaties zijn statisch per input, dus deze zijn ook onderdeel van het bord.
<br>

Paden zijn in dit geval een verzameling van coördinaten die opeenvolgend leiden tot het eindpunt. Paden bevatten wires en een cost (namelijk de hoeveelheid wires), maar er is voor gekozen om paden en/of nets niet een eigen klasse te geven aangezien de cost van een net-configuratie ook achteraf te berekenen is. Een pad/net is dan niets anders dan een verzameling coördinaten. Wel is het zo dat een chip-print een bepaalde verzameling van nets kan bevatten, bijvoorbeeld als deeloplossing. Om nets toegankelijk te houden, en ook per duo van gates toegang te hebben tot het bijbehorende net op een bord (als deze is gemaakt) worden nets in het bord opgeslagen door middel van een dictionary met als key een gate-duo en als value het bijbehorende net. Weet een algoritme een net niet te maken, dan komt er als value "False" te staan bij dat duo van gates in het bord wat wordt gebruikt.
<br>

Ten slotte is er een klasse toegevoegd voor nodes. Aangezien deze alleen relevant is voor het a-star algoritme wat in deze case is ontwikkeld, zullen nodes bij de beschrijving van a-star verder worden toegelicht.
<br>







# Beschrijving van de algoritmen

## Wat algemene informatie

### Moves

Elk van de ontwikkelde algoritmen zijn algoritmen die nets aan het bord toevoegen door stap voor stap een pad te maken van een gate naar een ander gate. Hiervoor is het belangrijk om duidelijk te maken wat de regels zijn bij het zetten van een stap, aangezien deze regels voor elk van de algoritmen worden gebruikt.
<br>

Wordt er vanaf een gate een stap gezet, dan wordt er gekozen uit 6 mogelijke richtingen, namelijk: Noord, Oost, Zuid, West, Omhoog, Omlaag (in die exacte volgorde). Een move is <i>niet</i> legaal als:

<ul>
  <li>Deze buiten de dimensies van het bord stapt</li>
  <li>Deze op een gate stapt die niet het doel is van de net</li>
  <li>Deze op een coördinaat stapt dat al is bezocht door het huidige pad (met uitzonderingen, zie a_star)</li>
  <li>Deze overlap veroorzaakt</li>
</ul>

### Sorteren van de netlist

Nog een eigenschap die we hebben bekeken is de volgorde van gevraagde nets in de netlist die wordt gebruikt. De door ons gebruikte algoritmen kregen voor de standaard volgorde van de netlists niet altijd een oplossing. Dit kwam in sommige gevallen doordat er een grote net veel ruimte van het bord in beslag nam en ervoor kon zorgen dat gates werden ingesloten en geen uitgaande nets meer konden maken.<br>
Naar onze verwachting zouden er betere oplossingen uit de algoritmen volgen als de kortste gevraagde nets (met maar weinig afstand tussen de gates) eerst worden gemaakt. Kleine nets nemen namelijk minder ruimte in beslag voor overige nets die nog gemaakt moeten worden.<br>
Na het implementeren van een sorteerfunctie die de netlist kan sorteren op afstand tussen de gates (euclidian) merkten wij dat de algoritmen vaker meer nets konden maken en dat gates minder snel werden ingesloten. <br>
Voor grotere oplossingen was er echter nog een probleem. De meest gebruikte ruimte in een chip-print is het midden. Veel connecties tussen gates, zeker als deze aan tegenovergestelde kanten van de chip-print liggen, gebruiken de ruimte in het midden.<br>
Om deze reden hebben we besloten om de volgorde ook rekenening te laten houden met de afstand van de gates per duo tot het midden. Deze sorteerfunctie bepaalt het midden van het bord (op de onderste laag aangezien alle gates op de onderste laag liggen) en telt de afstand van elk van de gates in een duo tot het middelpunt op. Het algoritme houdt ook nogsteeds rekening met de afstand tussen gates en telt deze op bij de afstanden tussen de gates en het middelpunt. Zo volgt er een gewogen waarde die prioriteit geeft aan gevraagde gate-connecties die dicht bij het bord liggen, en connecties met gates die erg dicht bij elkaar liggen. Dit resulteerde in nog iets betere oplossingen, voornamelijk voor de grotere problemen.



## Breadth-first search (BFS)
Het BFS algoritme is een zoekalgoritme dat vanaf een beginpunt kijkt bij elke vertakking of het de oplossing is en vervolgens voor elk van die vertakkingen dit proces uitvoert totdat de gewenste oplossing gevonden is. Het zoek algoritme breidt op deze manieer alle mogelijkheden van paden uit in alle vertakkings richtingen en slaat deze paden op totdat het einddoel is bereikt. Het algoritme houd er rekening mee dat paden elkaar niet kruizen en er dus ook geen overlap van paden kan ontstaan. Tevens kunnen paden niet over gates heen lopen. Verder gebruikt dit zoek algoritme geen informatie over het zoekprobleem tijdens het zoeken.

## Random algoritme
Het random algoritme is een zoekalgoritme dat vanaf een beginpunt random in de diepte elke keer 1 vertakking onderzoekt en vervolgens hierna voor die vertakking ook 1 vertakking onderzoekt. Het algoritme kiest een tak en doorzoekt deze dus zo ver mogelijk, zonder terug te keren op vorige stappen. Als het algoritme vastloopt worden alle paden verwijdert en begint het algoritme weer vanaf het startpunt. Het algoritme houd er rekening mee dat paden elkaar niet kruizen en er dus ook geen overlap van paden kan ontstaan. Tevens kunnen paden niet over gates heen lopen.
Er is gekozen om alle paden te verwijderen bij het vastlopen omdat in de helft van de gevallen een pad verwijderen en weer opnieuw aanleggen weer resulteerde in het vastlopen van het algortime. Opnieuw beginnen heeft een hogere kans van slagen. 

## A-star algoritme
Het A-star algoritme maakt nets door alleen de meest veelbelovende paden uit te breiden vanaf het startpunt. 
Op elke stap wordt in elke richting gekeken. Vervolgens worden er voor elk van de locaties waar naartoe bewogen kan worden een <i>node</i> gemaakt, een datastructuur die het algoritme in staat stelt een soort kaart te maken van zijn omgeving.<br>
Een node bevat een aantal dingen:

<ul>
  <li>De coordinaten van zijn eigen locatie</li>
  <li>De locatie van de node van waar er naar deze node is uitgebreid (oftewel zijn "parent")</li>
  <li>een "g"-waarde. Deze representeerd de afstand van het startpunt <i>tot</i> deze node </li>
  <li>een "h"-waarde. Deze representeert de afstand van deze locatie <i>tot</i> het eindpunt</li>
  <li>een "f"-waard. Deze representeert de optelsom van de bovenste twee waarden</li>
  <li>Een boolean genaamd <i>intersection</i> die vertelt of er op dit punt een intersectie heeft plaatsgevonden</li>
</ul>

Wordt er een nieuwe node gemaakt, dan krijgt hij deze waarden toegewezen. De heuristic "h" is te bepalen met euclidian afstand tot het eindpunt en manhattan afstand tot het eindpunt. Welke van de twee tot efficientere uitkomsten leidt verschilt per oplossing. Vervolgens, als het algoritme zijn volgende stap gaat zetten, wordt de keuze van welke node wordt uitgebreid bepaald door de f-waarde. Dit representeert het meest veelbelovende pad, omdat dit punt het dichtst is bij het startpunt, en het dichtst bij het eindpunt, en dus veelbelovend is voor het leveren van een zo kort mogelijk pad vergeleken met de andere opties. Zo wordt het algoritme gestuurd om moves te maken richting het eindpunt. Als het eindpunt wordt bereikt wordt er opeenvolgend gekeken naar parents van nodes tot het startpuntn wordt bereikt, en zo volgt er een pad. Op deze manier hoeven er ook geen onvolledige paden begehouden te worden in het geheugen.<br>

Soms (vaak) kan het gebeuren dat er naar een node wordt uitgebreid die al is bekeken door het algoritme. Is dit punt al bekeken, dan bestaat er in de ogen van het algoritme al een pad naar dit punt. Slechts 1 van de twee opties wordt bewaard, door de g-waarde (afstand van start tot dit punt) van de al bestaande node en de nieuwe node te vergelijken. Is de g-waarde van de node die al bestaat kleiner, dan bestaat er al een ander korter pad tot dat punt. Dat maakt het nieuwe pad tot dat punt overbodig, en deze wordt dan ook weggegooit. Deze keuze wordt gemaakt door te bepalen waar de node op dat punt naar wijst, ofwel wat hij als zijn parent beschouwt. <br>

Ten slotte staat dit algoritme wel intersecties toe. Intersecties kosten 300 (ze verhogen de totale kosten van het bord met 300). Dit betekent dat een pad dat een intersectie maakt pas interessant is als er geen andere paden met een omweg korter dan 300 wires gemaakt kunnen worden. Hiervoor kan heel handig de g-waarde gebruikt worden. Maakt het algoritme een stap, dan is de g-waarde voor het nieuwe punt de g-waarde van zijn parent + 1 (één stap kost 1 in deze case). Maakt het algoritme echter een stap met een intersectie, dan wordt zijn g-waarde verhoogt met 300. Dit zorgt ervoor dat het uitbreiden van dit pad een flink verlaagde prioriteit heeft, en dat dit pad pas uitgebreid zal worden als andere opties meer dan 300 wires ver zijn.


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
  <li><b>tt</b>: Total Time: Hier hoort het aantal runs die uitgevoert moet worden.
                 (aantal ints)</li>
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

Daarnaast wordt ook het beste geval van elk van deze statistieken verzameld..<br>

Elke individuele run van het algoritme zal worden aangekondigd door het printen van "run: " gevolgd door het nummer van de huidige run, en voor elke afgemaakte run zullen de bijbehorende statistieken per run op een nieuwe regel worden afgeschreven in output/output_[gebruikte algoritme].csv. Enkele gemiddelden en de beste statistieken worden ook nog uitgeschreven naar
stdout.