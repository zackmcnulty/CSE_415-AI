README.txt

This is Version 8a (released Feb. 23, 2018) of the support code
for Assignment 5 in CSE 415, University of Washington, Winter 2018.

This is minor bug-fix and enhancement release. The last major release
was the Feb. 18 code release.  The file versions and starter code
numbers are being unified in this release.  It's being called version 8a.

Written by S. Tanimoto, with feedback from R. Thompson, for CSE 415
and from students in the class.

Main update in this version: optional display of the golden path.
This can be enabled on the rewards menu.

To start the GUI, type the following, in the same folder
as the code.

python3 TOH_MDP.py

All files here except YourUWNetID_VI.py are different from those in
the first release.

TOH_MDP.py and Vis_TOH_MDP.py have been updated in this version since
the previous version (the Feb. 18 version).  Corrections have been
made in the functions that compare policies, state values and Q values.

In the previous version:
The sample script was updated to suggest how to automate
setup for doing Q-Learning experiments.

The user can only show a policy when it is safe (a policy can be extracted),
assuming your extract_policy methods work.

Policy display is persistent with automatic updating whenever Q values
change.

Independent policies are stored and displayed... one for VI and one for
QL.  This also means you can view both at the same time, in different
colors.

Misc. improvements, related to the manual user driving, etc.

