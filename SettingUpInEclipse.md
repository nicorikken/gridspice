# Instructions #
  1. Select the Source tab on the GridSpice Google Code page.
  1. Choose “interface” under the repository tab.
  1. Use either the resulting Option 1 or Option 2 to clone the repository.
  1. Open Eclipse.
  1. Open Help->Install New Software and search for the following download links, as shown in the succeeding image:
    1. http://download.eclipse.org/egit/updates
    1. http://dl.google.com/eclipse/plugin/3.7
_Note: If you do not have the plug-ins that result from the search, then you will need to download them._
<img src='http://gridspice.googlecode.com/files/InstallingPlugins.png' height='400' width='600'> <br />
</li></ul></li></ul><blockquote>6. After the installation process has completed, import the Git repository into the Eclipse workspace as follows:<br>
<ol><li>Open the GIT Repositories View (Window->Show View -> Git Repositories)
    1. Choose the option "Add existing Git Repository...." and add the gridspice.interface repository that you had downloaded in step 3.
    1. Go to File->Import->Git->Projects From Git and select the repository that you added in the previous step. Select the "Next" option until the process is complete.
> `7. Expand the project in the Package Explorer Bar (Click on the triangle to the left of the project), and right-click the package "src," and then click on Build Path->Set As Source Folder.`

> 8. Right-click the package "war", and then click on Build Path->Exclude.

> 9. Right click on the project in the Package Explorer bar, click on Build Path->Configure Build Path and add the following libraries, as shown in the succeeding two images:
    1. JRE System Library (Mac) | JDK (Windows)
    1. App Engine SDK
    1. GWT SDK
<img src='http://gridspice.googlecode.com/files/ScreenShot1.png' height='400' width='600'>
<img src='http://gridspice.googlecode.com/files/ScreenShot2.png' height='400' width='600'> <br />
</li></ol>> `10. Add JAR files that were included with the project. Right click on the project in the Package Explorer bar, click on Build Path->Configure Build Path and add all of the jar files contained under the .lib folder, as follows:`
    1. Click on "Add Jars...."
    1. `Under .lib, select all JAR files except for those in the folders containing names with "app-engine-sdk" or   "gwt-2." In the screen shot below, all of the jar files, excluding the ones in folders containing those  names, have been added.`
<img src='http://gridspice.googlecode.com/files/Adding Jars 1.png' height='400' width='600'>
<img src='http://gridspice.googlecode.com/files/Adding Jars 2.png' height='400' width='600'> <br />
</blockquote><blockquote><code>11. To run, right-click on the project in the Package Explorer bar:</code>
<ol><li>Click on Debug As -> Web Application.<br>
</li><li>Select Imageviewer.html<br>
</li><li><code>Double click the link that shows up in the Deployment Mode Panel (at the bottom of the screen) when the program is done compiling.</code>
<img src='http://gridspice.googlecode.com/files/Running 1.png' height='400' width='600'>
<img src='http://gridspice.googlecode.com/files/Running 2.png' height='400' width='600'>
<img src='http://gridspice.googlecode.com/files/Running 3.png' height='400' width='600'>