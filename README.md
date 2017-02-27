This is a demo application using relatively minimalistic approach to create a database-driven single-page client logic application.
While not using recent frameworks and relying heavily on jquery, it is still useful on how simple (but expandable) legacy applications may have worked.
Backbone.js is used for client-side logic while a restful api and static files server is provided by flask or django (both versions present) with a mysql-compatible database containing the data. Written mostly for own experience broadening and uploaded for demonstration purposes.

Client-side javascripts are either minimized (flask version) or compiled from separate files (django version) using compile.py scripts in either directory. You will need to provide paths to the html and js minifier (available here http://yui.github.io/yuicompressor/ and here https://developers.google.com/closure/compiler/) applications for the minification to work.

The initialization is done by creating a database, running either inittables.sql and filltables.sql (flask, as source inside the database) or initdefaults.py (django) renaming the sample_config.py (flask) or sample_settings.py (django, needs to be done after database configuration) and providing your database name and credentials in the respective settings files. Client-side javascripts need to be compiled before launching.
Databases do need to be separate for separate versions.
