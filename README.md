exceptional_clarity
===================

Here's an example - try an operation on incomatible types and Exceptional Clarity will try to give you some useful feedback:

    In [1]: "hello" / 42
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-2-55c1fb77a219> in <module>()
    ----> 1 "hello" / 42

    TypeError: unsupported operand type(s) for /: 'str' and 'int'
    <EXCEPTIONALCLARITY>: You tried to do an operation on two types that don't allow that operation, are you sure you're doing something sensible?


Installing
----------

Check this project out to a local folder. Go to the IPython profile (on Linux it is probably `~/.ipython/profile_default`) and go into the `startup` subfolder. Create a symbolic link from `exceptional_clarity.py` into the startup folder:

    $ ~/.ipython/profile_default/startup $ ln -s ~/workspace/personal_projects/exceptional_clarity/exceptional_clarity.py

Now in the startup directory you'll have a link, IPython checks this `startup` directory on startup.

    ian@ian-Latitude-E6420 ~/.ipython/profile_default/startup $ ls -la
    total 24
    drwxr-xr-x 3 ian ian 4096 Aug 19 13:02 .
    drwxr-xr-x 8 ian ian 4096 Aug 19 13:06 ..
    lrwxrwxrwx 1 ian ian   80 Aug 19 13:02 exceptional_clarity.py -> /home/ian/workspace/personal_projects/exceptional_clarity/exceptional_clarity.py
   
To uninstall just delete the link in `startup`.

When you start IPython you'll get a short message telling you it started successfully:

    $ ipython
    Python 3.4.1 |Anaconda 2.0.1 (64-bit)| (default, May 19 2014, 13:02:41) 
    Type "copyright", "credits" or "license" for more information.
    IPython 2.1.0 -- An enhanced Interactive Python.
    Anaconda is brought to you by Continuum Analytics.
    Please check out: http://continuum.io/thanks and https://binstar.org
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.
    Loaded <EXCEPTIONALCLARITY> extension

It is the `Loaded <EXCEPTIONALCLARITY> extension` that you're looking for.
