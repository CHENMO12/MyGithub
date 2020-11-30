
myBase Desktop Ver 7.x -- Readme
__________________________________________________________



CONTENTS
============================

1. What's myBase
2. System Requirements
3. Installation
4. Uninstallation
5. Upgrade existing .nyf databases from v6.x to v7.x 
6. Contact Information



1. What's myBase
============================

myBase is a powerful yet easy-to-use information management software 
that allows entry of unstructured text, webpages, images, documents, 
emails and even arbitrary files without regard to length or format. 
All information is automatically compressed and stored in the tree 
structured outline form. Unlike traditional database programs, myBase 
accepts text input like a word processor, and provides better methods 
for capturing, editing, organizing, retrieving, searching and sharing 
information.

With myBase, you get a personal knowledge base tool, research database 
program, personal information organizer, notes manager, mind manager, 
documentation tool, book writing tool, presentation tool, ebook maker, 
to-do list, customer data management, genealogy software, notes taker, 
address book, photo album, diary keeper, URL organizer, file organizer, 
rich text editor, and much much more. All this in a footprint of less 
than 60MB and will make your life easier.

myBase Desktop 7 is now available for GNU/Linux, Mac OS X and Windows.

For detailed info about myBase, please visit: www.wjjsoft.com/mybase



2. System Requirements
=======================

To run myBase Desktop Ver 7.x, you will need a PC (or Tablet PC) 
running GNU/Linux, Mac OS X or Windows XP+.



3. Installation
==============================================

For GNU/Linux, extract the downloaded .tar package into your home directory,
then you can run the command line './myBase.run &' from the directory in a
Terminal; You might also want to create a launcher for myBase on the X11 
desktop for quick launch.

Note that with different distributions of GNU/Linux, you may need to 
manually install additional packages to resolve the shared library 
dependencies. To check out the library dependencies for myBase 7.x, 
open a Terminal, change to the program's directory, and run the command 
'ldd myBase'.

In the case of "Error while loading shared libraries: libpng12.so.0" on Ubuntu 
(e.g. Ubuntu 18.04) you'll need first to download the library from the packages 
website ( https://packages.ubuntu.com/xenial/amd64/libpng12-0/download )
and then manually install it by running a command like this:
'sudo dpkg -i libpng12-0_1.2.54-1ubuntu1.1_amd64.deb'

For Mac OS X, open the downloaded .dmg package file, simply double-click on 
the program's icon to launch it. For the convenience of launching it from 
Launchpad, please drag the program's icon and drop into the system's
Applications folder, then it will appear on the Launchpad.

For Windows, just run the downloaded .exe self-extractable setup program and 
then follow the instructions; You'll need to select the install directory and 
program group name; Then you can double click on the program's icon to start it 
from Desktop or from the Start menu.



4. Uninstallation
============================

For GNU/Linux, simply remove the program's directory.

For Mac OS X, trash the program from the Applications folder.

For Windows, select the "Uninstall myBase Desktop 7" menu item from 
the Start menu, and press "Yes" to confirm.

Note that you will need to create backup for your own .nyf database files 
created with myBase before uninstalling or removing the program's folder.



5. Upgrade existing .nyf databases from v6.x to v7.x
========================================================

From version 7.0 on, myBase has switched over to save text content in HTML 
for better cross-platform support, with no support for RTF formats any more.
If you have existing .nyf databases generated with previous version 4/5/6.x
of myBase for Windows, and would like to upgrade to v7.x, please try to 
upgrade the database file format, by selecting the menu item
"File - Maintenance - Replicate from RTF to HTML ..." within myBase v6.5.1+
for Windows. The generated .nyf databases will work smoothly with myBase 
v7.x on Linux, Mac OS X and Windows.

Note that unlike RTF text format, the HTML text format doesn't support OLE 
objects embedding into the text content; If any RTF content contains OLE 
objects, they will be converted into thumbnail images in the resulting HTML 
documents, with no support of double-clicking on OLE objects to view or edit 
them any more.



6. Contact Information
=======================

Any questions, comments and suggestions, please contact us at:

info@wjjsoft.com
sales@wjjsoft.com
support@wjjsoft.com




__________________________________________________________

Copyright 1998-2019 Wjj Software. All Rights Reserved.
http://www.wjjsoft.com/mybase

