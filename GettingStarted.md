# Introduction #

This page gives a brief tutorial on running a simulation using GridSpice.


# Load Project #
First you need to load the project.  Click the "load project" button shown below.  You should have several sample projects loaded into your account.  If you do not, contact support.
<br />
<img src='http://www.stanford.edu/~anderk57/gridspice/process/step1.jpg' height='400' width='600'>

<h1>Load Editor</h1>
Once you have selected your project, you should load an editor for the schematic you wish to change.  In this example, we will edit one of the distribution schematics in the project.  Click the "Editor" button under the distribution section.  To use map mode, click the "Map" button for the desired schematic, to use the scripting/explorer interface click "Explorer".<br>
<br />
<img src='http://www.stanford.edu/~anderk57/gridspice/process/step2.jpg' height='400' width='600'>

<h1>Add Triplex Meter</h1>
Next we will add a triplex meter to the map.  A Triplex Meter is the basic grid element that loads attach to.  After you add a Triplex Meter, you can attach loads such as houses, office buildings, etc.  Select "Triplex Meter" from the "distribution network" accordion in the left panel.<br>
<img src='http://www.stanford.edu/~anderk57/gridspice/process/step4.jpg' height='400' width='600'>

<h1>Add Powerline</h1>
You must connect the triplex meter to the grid.  Select the a wire type from the accordion menu on the left.  Click once on the Triplex Meter and click again on the upstream network element.<br>
<img src='http://www.stanford.edu/~anderk57/gridspice/process/step5.jpg' height='400' width='600'>
<img src='http://www.stanford.edu/~anderk57/gridspice/process/step6.jpg' height='400' width='600'>

<h1>Add Child Object</h1>
Now you can attach a load to the meter.  Click the newly added node in order to bring up the menu.  You may need to deselect the power line button on the left if you have not already.<br>
<br />
<img src='http://www.stanford.edu/~anderk57/gridspice/process/step7.jpg' height='400' width='600'>

After clicking the Triplex meter icon, you will see this page.  Select "add child object".  A menu will appear showing all eligable child objects (loads).  Select an object.<br>
<br />
<img src='http://www.stanford.edu/~anderk57/gridspice/process/step8.jpg' height='400' width='600'>



<h1>Run Simulation / View Results</h1>
First select "save" on the left to write your changes to the database.  Next select the blue "Run" icon to begin the simulation.  This step may take some time.  Once the simulation is complete, you can click "Download" to view results for any tape elements in the network.<br>
<br />
<img src='http://www.stanford.edu/~anderk57/gridspice/process/step9.jpg' height='400' width='600'>