# Introduction #
The current app engine version is deployed as a "backend" so that requests can take more than 30 seconds.  When the interface builds the .glm file, it will take ~30 seconds to complete.  We could split up the jobs, but deploying it as a "backend" side steps the issue for now.


# Details #
You can deploy with the following command from your repo directory, where dir is "war" and backend is "gridspicebackend"
appcfg backends 

&lt;dir&gt;

 update [backend](backend.md)