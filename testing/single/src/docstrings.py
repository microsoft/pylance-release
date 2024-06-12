# This file is for testing different types of docstrings and verifying they display
# correctly.
# Try it with `python.analysis.supportRestructuredText` both true and false. 
import numpy as np

# Hover over zeroes and ensure the markdown looks correct.
# `Correct` is subjective, but basically ensure that the markdown looks like
# you would want it to look. There isn't weird lines appearing in the middle of things (like a table not displaying)
# There isn't weird characters appearing in the middle of things
# Parameters are consistently represented
# Gifs/Links/Images show up
z = np.zeros([1, 2, 3])

# Hover over take and ensure the markdown looks correct.
t = np.take(z, [0])

# Goto declaration on np and hover over all of the methods found there.
# Ensure that all methods (which have docstrings) display markdown that is rendered correctly

# Hover over each of these functions and verify they're rendering output in a way that makes sense (this is kind of subjective)
def pythonorg():
    """
    This is Python version 3.14.0 alpha 0
    =====================================

    .. image:: https://github.com/python/cpython/workflows/Tests/badge.svg
        :alt: CPython build status on GitHub Actions
        :target: https://github.com/python/cpython/actions

    .. image:: https://dev.azure.com/python/cpython/_apis/build/status/Azure%20Pipelines%20CI?branchName=main
        :alt: CPython build status on Azure DevOps
        :target: https://dev.azure.com/python/cpython/_build/latest?definitionId=4&branchName=main

    .. image:: https://img.shields.io/badge/discourse-join_chat-brightgreen.svg
        :alt: Python Discourse chat
        :target: https://discuss.python.org/


    Copyright © 2001-2024 Python Software Foundation.  All rights reserved.

    See the end of this file for further copyright and license information.

    .. contents::

    General Information
    -------------------

    - Website: https://www.python.org
    - Source code: https://github.com/python/cpython
    - Issue tracker: https://github.com/python/cpython/issues
    - Documentation: https://docs.python.org
    - Developer's Guide: https://devguide.python.org/

    Contributing to CPython
    -----------------------

    For more complete instructions on contributing to CPython development,
    see the `Developer Guide`_.

    .. _Developer Guide: https://devguide.python.org/

    Using Python
    ------------

    Installable Python kits, and information about using Python, are available at
    `python.org`_.

    .. _python.org: https://www.python.org/

    Build Instructions
    ------------------

    On Unix, Linux, BSD, macOS, and Cygwin::

        ./configure
        make
        make test
        sudo make install

    This will install Python as ``python3``.

    You can pass many options to the configure script; run ``./configure --help``
    to find out more.  On macOS case-insensitive file systems and on Cygwin,
    the executable is called ``python.exe``; elsewhere it's just ``python``.

    Building a complete Python installation requires the use of various
    additional third-party libraries, depending on your build platform and
    configure options.  Not all standard library modules are buildable or
    useable on all platforms.  Refer to the
    `Install dependencies <https://devguide.python.org/getting-started/setup-building.html#build-dependencies>`_
    section of the `Developer Guide`_ for current detailed information on
    dependencies for various Linux distributions and macOS.

    On macOS, there are additional configure and build options related
    to macOS framework and universal builds.  Refer to `Mac/README.rst
    <https://github.com/python/cpython/blob/main/Mac/README.rst>`_.

    On Windows, see `PCbuild/readme.txt
    <https://github.com/python/cpython/blob/main/PCbuild/readme.txt>`_.

    To build Windows installer, see `Tools/msi/README.txt
    <https://github.com/python/cpython/blob/main/Tools/msi/README.txt>`_.

    If you wish, you can create a subdirectory and invoke configure from there.
    For example::

        mkdir debug
        cd debug
        ../configure --with-pydebug
        make
        make test

    (This will fail if you *also* built at the top-level directory.  You should do
    a ``make clean`` at the top-level first.)

    To get an optimized build of Python, ``configure --enable-optimizations``
    before you run ``make``.  This sets the default make targets up to enable
    Profile Guided Optimization (PGO) and may be used to auto-enable Link Time
    Optimization (LTO) on some platforms.  For more details, see the sections
    below.

    Profile Guided Optimization
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^

    PGO takes advantage of recent versions of the GCC or Clang compilers.  If used,
    either via ``configure --enable-optimizations`` or by manually running
    ``make profile-opt`` regardless of configure flags, the optimized build
    process will perform the following steps:

    The entire Python directory is cleaned of temporary files that may have
    resulted from a previous compilation.

    An instrumented version of the interpreter is built, using suitable compiler
    flags for each flavor. Note that this is just an intermediary step.  The
    binary resulting from this step is not good for real-life workloads as it has
    profiling instructions embedded inside.

    After the instrumented interpreter is built, the Makefile will run a training
    workload.  This is necessary in order to profile the interpreter's execution.
    Note also that any output, both stdout and stderr, that may appear at this step
    is suppressed.

    The final step is to build the actual interpreter, using the information
    collected from the instrumented one.  The end result will be a Python binary
    that is optimized; suitable for distribution or production installation.


    Link Time Optimization
    ^^^^^^^^^^^^^^^^^^^^^^

    Enabled via configure's ``--with-lto`` flag.  LTO takes advantage of the
    ability of recent compiler toolchains to optimize across the otherwise
    arbitrary ``.o`` file boundary when building final executables or shared
    libraries for additional performance gains.


    What's New
    ----------

    We have a comprehensive overview of the changes in the `What's New in Python
    3.13 <https://docs.python.org/3.13/whatsnew/3.13.html>`_ document.  For a more
    detailed change log, read `Misc/NEWS
    <https://github.com/python/cpython/tree/main/Misc/NEWS.d>`_, but a full
    accounting of changes can only be gleaned from the `commit history
    <https://github.com/python/cpython/commits/main>`_.

    If you want to install multiple versions of Python, see the section below
    entitled "Installing multiple versions".


    Documentation
    -------------

    `Documentation for Python 3.13 <https://docs.python.org/3.13/>`_ is online,
    updated daily.

    It can also be downloaded in many formats for faster access.  The documentation
    is downloadable in HTML, PDF, and reStructuredText formats; the latter version
    is primarily for documentation authors, translators, and people with special
    formatting requirements.

    For information about building Python's documentation, refer to `Doc/README.rst
    <https://github.com/python/cpython/blob/main/Doc/README.rst>`_.


    Testing
    -------

    To test the interpreter, type ``make test`` in the top-level directory.  The
    test set produces some output.  You can generally ignore the messages about
    skipped tests due to optional features which can't be imported.  If a message
    is printed about a failed test or a traceback or core dump is produced,
    something is wrong.

    By default, tests are prevented from overusing resources like disk space and
    memory.  To enable these tests, run ``make buildbottest``.

    If any tests fail, you can re-run the failing test(s) in verbose mode.  For
    example, if ``test_os`` and ``test_gdb`` failed, you can run::

        make test TESTOPTS="-v test_os test_gdb"

    If the failure persists and appears to be a problem with Python rather than
    your environment, you can `file a bug report
    <https://github.com/python/cpython/issues>`_ and include relevant output from
    that command to show the issue.

    See `Running & Writing Tests <https://devguide.python.org/testing/run-write-tests.html>`_
    for more on running tests.

    Installing multiple versions
    ----------------------------

    On Unix and Mac systems if you intend to install multiple versions of Python
    using the same installation prefix (``--prefix`` argument to the configure
    script) you must take care that your primary python executable is not
    overwritten by the installation of a different version.  All files and
    directories installed using ``make altinstall`` contain the major and minor
    version and can thus live side-by-side.  ``make install`` also creates
    ``${prefix}/bin/python3`` which refers to ``${prefix}/bin/python3.X``.  If you
    intend to install multiple versions using the same prefix you must decide which
    version (if any) is your "primary" version.  Install that version using
    ``make install``.  Install all other versions using ``make altinstall``.

    For example, if you want to install Python 2.7, 3.6, and 3.13 with 3.13 being the
    primary version, you would execute ``make install`` in your 3.13 build directory
    and ``make altinstall`` in the others.


    Release Schedule
    ----------------

    See :pep:`719` for Python 3.13 release details.


    Copyright and License Information
    ---------------------------------


    Copyright © 2001-2024 Python Software Foundation.  All rights reserved.

    Copyright © 2000 BeOpen.com.  All rights reserved.

    Copyright © 1995-2001 Corporation for National Research Initiatives.  All
    rights reserved.

    Copyright © 1991-1995 Stichting Mathematisch Centrum.  All rights reserved.

    See the `LICENSE <https://github.com/python/cpython/blob/main/LICENSE>`_ for
    information on the history of this software, terms & conditions for usage, and a
    DISCLAIMER OF ALL WARRANTIES.

    This Python distribution contains *no* GNU General Public License (GPL) code,
    so it may be used in proprietary projects.  There are interfaces to some GNU
    code but these are entirely optional.

    All trademarks referenced herein are property of their respective holders.
    """

def test_googlestyledocs():
    """
    Available subpackages
    ---------------------
    lib
        Basic functions used by several sub-packages.
    random
        Core Random Tools
    linalg
        Core Linear Algebra Tools
    fft
        Core FFT routines
    polynomial
        Polynomial tools
    testing
        NumPy testing tools
    distutils
        Enhancements to distutils with support for
        Fortran compilers support and more.

        Some more text in the another paragraph.
    """
    print('hi!')

def plainstring():
    """
    Section
    -------
    Foo
       Bar
    
    Biz
       Baz
    """

def googlestring_withreturn():
    """
    Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/
    """

def bulleted_list():
    """
    Bulleted list
    -------------
    * Item1
        
        * SubItem
    
    * Item2
        
        * SubItem
    """

def googlewithcomplextypes():
    """
    Example function with types documented in the docstring.

    Args:
        param1 (int|bool): The first parameter.
        param2 (list[str] with others): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.
    """

def epytext_imread():
    """
imread(filename[, flags]) -> retval
.   @brief Loads an image from a file.
.   @anchor imread
.   
.   The function imread loads an image from the specified file and returns it. If the image cannot be
.   read (because of missing file, improper permissions, unsupported or invalid format), the function
.
.   Currently, the following file formats are supported:
.   
.   -   Windows bitmaps - \\*.bmp, \\*.dib (always supported)
.   -   JPEG files - \\*.jpeg, \\*.jpg, \\*.jpe (see the *Note* section)
    """

def epytextwithparams():
    """
    Return the x intercept of the line M{y=m*x+b}.  The X{x intercept}
    of a line is the point at which it crosses the x axis (M{y=0}).

    This function can be used in conjuction with L{z_transform} to
    find an arbitrary function's zeros.

    @type  m: number
    @param m: The slope of the line.
    @type  b: number
    @param b: The y intercept of the line.  The X{y intercept} of a
                line is the point at which it crosses the y axis (M{x=0}).
    @rtype:   number
    @return:  the x intercept of the line M{y=m*x+b}.
    """

def htmlinsidecode():
    '''hello  `<code>`'''


def resttable():
    """
    =============== =========================================================
    Generator       Description
    --------------- ---------------------------------------------------------
    Generator       Class implementing all of the random number distributions
    default_rng     Default constructor for ``Generator``
    =============== =========================================================
    """

def resttableindented():
    """    
    data :

    dtype : str, np.dtype, or ExtensionDtype, optional

        ============================== =====================================
        Scalar Type                    Array Type
        ============================== =====================================
        :class:`pandas.Interval`       :class:`pandas.arrays.IntervalArray`
        :class:`pandas.Period`         :class:`pandas.arrays.PeriodArray`
        ============================== =====================================
    """

def epytext_moreparams():
    """
    
    @param 'original:str' or 'original:list': original string to compare
    @param 'new:str': the new string to compare
    @return 'int': levenshtein difference
    @return 'list': levenshtein difference if list
    """

def asciiart():
    """
    
    ::

         #####    #####             ####
        ##   ##  ##   ##           ##             ####
        ##  ##   ##  ##           ##                 #
        #####    #####   ##   ##  ##               ##
        ##  ##   ##       ## ##   ##                 #
        ##   ##  ##        ###    ##              ###
        ##   ##  ##        ##      #####
     -------------------- ## ------------------------------------------
                         ##
    
    Remote Python Call (RPyC)
    """
def justpipes():
    """
    This is a paragraph.

    | This is a line
    | with another line
    """

def fullrst():
    """
    Panel is a high level app and dashboarding framework
    ====================================================

    Works with the tools you know and ❤️.

    `Getting Started<https://panel.holoviz.org>`_ | `Discourse`_ | `Github`_ | `Twitter`_ |
    `LinkedIn`_

    Interactive models with ``.bind``
    ---------------------------------

    .. figure:: https://user-images.githubusercontent.com/42288570/150686594-21b03e55-79ef-406b-9e61-1764c6b493c3.gif
        :alt: Interactive Model App

        Interactive Model App

    You can use Panels ``.bind`` to bind your models to widgets.

    .. code:: python

        import panel as pn

        color = "#C43F66"

        pn.extension(sizing_mode="stretch_width", template="fast")


        def model(a, b, emoji):
            result = "#" + (emoji * a) + " + " + (emoji * b) + " = " + (emoji * (a + b))
            return result

        pn.pane.Markdown("## Input", margin=(5, 10)).servable(area="sidebar")
        input1 = pn.widgets.RadioButtonGroup(value=1, options=[1, 2, 3], button_type="success", name="A").servable(area="sidebar")
        input2 = pn.widgets.IntSlider(value=2, start=0, end=3, step=1, margin=(20, 10)).servable(area="sidebar")

        interactive_add = pn.bind(model, a=input1, b=input2, emoji="⭐")
        pn.panel(interactive_add).servable(area="main", title="My interactive MODEL")

        pn.state.template.param.update(site="Panel", accent_base_color=color, header_background=color)

    You can serve your app via

    .. code:: bash

        $ panel serve 'script.py' --autoreload
        2022-01-23 15:00:31,373 Starting Bokeh server version 2.4.2 (running on Tornado 6.1)
        2022-01-23 15:00:31,387 User authentication hooks NOT provided (default user enabled)
        2022-01-23 15:00:31,389 Bokeh app running at: http://localhost:5006/script

    The file can be a ``.py`` script or ``.ipynb`` notebook.

    Try changing the return value of the function. Panel will magically ✨
    understand how to show the objects you know and ❤️.

    | This includes `Bokeh`_,
    | `HoloViews`_,
    | `Matplotlib`_ and
    | `Plotly`_ figures.

    Interactive dataframes with ``.interactive``
    --------------------------------------------

    .. figure:: https://user-images.githubusercontent.com/42288570/150683991-9cece6a1-3751-42d2-8256-505f5deb12be.gif
        :alt: Interactive DataFrame App

        Interactive DataFrame App

    You can use `hvplot .interactive`_ to make your dataframes interactive.

    ```python import panel as pn import pandas as pd import hvplot.pandas

        color = “#0072B5” df = pd.DataFrame(data={“x”: [0, 1, 2, 3, 4], “y”: [0,
        2, 1, 3, 4]})

        pn.extension(sizing_mode=“stretch_width”, template=“fast”)

        pn.pane.Markdown(“## Selection”, margin=(10,
        10)).servable(area=“sidebar”) count =
        pn.widgets.RadioButtonGroup(value=5, options=[3, 4, 5], name=“Count”,
        button_type=“success”).servable(area=“sidebar”)

        interactive_df = df.interactive().head

    .. _Discourse: https://discourse.holoviz.org/
    .. _Github: https://github.com/holoviz/panel
    .. _Twitter: https://twitter.com/Panel_org
    .. _LinkedIn: https://www.linkedin.com/company/79754450
    .. _Bokeh: https://panel.holoviz.org/reference/panes/Bokeh.html#panes-gallery-bokeh
    .. _HoloViews: https://panel.holoviz.org/reference/panes/HoloViews.html#panes-gallery-holoviews
    .. _Matplotlib: https://panel.holoviz.org/reference/panes/Matplotlib.html#panes-gallery-matplotlib
    .. _Plotly: https://panel.holoviz.org/reference/panes/Plotly.html#panes-gallery-plotly
    .. _hvplot .interactive: https://hvplot.holoviz.org/user_guide/Interactive.html
    """

def paragraphs():
    """
    This is a paragraph.
    
    This is another paragraph. There should be some blank lines between them.
    """

def inlinemarkup():
    '''
    This is a paragraph with *italics* and **bolding**.

    This is a paragraph with `code`.
    '''

def termlist():
    """
    Term
        Definition

    Another term
        Another definition
    """

def list():
    '''
    * this is
    * a list

        * with a nested list
        * and some subitems

    * and here the parent list continues
    '''

def numberedlist():
    '''
    1. this is
    1. a list

        1. with a nested list
        1. and some subitems

    1. and here the parent list continues
    '''

def my_function(my_arg, my_other_arg):
    """
    A function just for me.

    :param my_arg: The first of my arguments.
    :param my_other_arg: The second of my arguments.
        more text on a second line

    :returns: A message (just for me, of course).
    """

def literalblock():
    """
    This is a normal text paragraph. The next paragraph is a code sample::

        It is not processed in any way, except
        that the indentation is removed.

        It can span multiple lines.

    This is a normal text paragraph again.
    """


def doctestblock():
    '''
    This next line is a doctest block. It needs a space

    >>> 1 + 1
    2
    '''

def normaltable():
    """
    +------------------------+------------+----------+----------+
    | Header row, column 1   | Header 2   | Header 3 | Header 4 |
    | (header rows optional) |            |          |          |
    +========================+============+==========+==========+
    | body row 1, column 1   | column 2   | column 3 | column 4 |
    +------------------------+------------+----------+----------+
    | body row 2             | ...        | ...      |          |
    +------------------------+------------+----------+----------+
    """

def simpletable():
    """
    ================ ============ =============
    Column 1         Column 2     Column 3
    ================ ============ =============
    Some text        Some more    Some more
    Another row      2            3
    ================ ============ =============
    """

def link():
    """
    Direct link
    `Link text <https://domain.invalid/>`_

    Next should be a ref
    `Link ref`_

    .. _Link ref: https://domain.invalid/

    This is a paragraph that contains `a link`_.

    .. _a link: https://domain.invalid/
    """

def sections():
    '''
    =================
    This is a heading
    =================
    -----------------
    This is a subheading
    -----------------
    *****************
    This is another heading
    *****************
    ^^^^^^^^^^^^^^^^^
    This is a subheading
    ^^^^^^^^^^^^^^^^^
    """""""""""""""""
    This is another heading
    """""""""""""""""
    '''

def strikethrough():
    """
    This is a paragraph with ~~strikethrough~~ text.
    """

def citation():
    """
    This is a paragraph with a citation [CIT2000]_.

    .. [CIT2000] This is a citation.
    """

def substitution():
    """
    The |biohazard| symbol must be used on containers used to
    dispose of medical waste.

    .. |biohazard| image:: https://thumb10.shutterstock.com/thumb_large/3673289/401411077/stock-vector-biohazard-sign-vector-illustration-eps-401411077.jpg
        :alt: biohazard
    """

def footnotes():
    """
    Lorem ipsum [#f1]_ dolor sit amet ... [#f2]_

    .. rubric:: Footnotes

    .. [#f1] Text of the first footnote.
    .. [#f2] Text of the second footnote.
    """
    
def format_example_func(a:str, b:int):
    """
    This function made expressly to show docstring formatting and nothing else
    
    For some reason the parsing has a really hard time when I write a docstring
    where both multiline docstrings and indentation exist simultaneously.

        Params:
            a: a string you want to do something with, who knows what it actually
               does this is just an example so people can call the help function
            b: another random arguement intended to showcase what changes when you
               combine indentation with multiline docstrings

        Returns:
            foo: I don't even know what this thing will return blah blah thingy
                 stuff stuff stuff.
    """

class Foo:
    """Does the thing.

    Attributes:
        bar (int): A short description
        buzz (str): A longer description that needs to be broken up over multiple lines,
            because there is additional context that I want to provide, and I don't
            want to go past the 88 line length limit for whatever reason.
    """
    bar: int
    buzz: str

def foo(a:int,b:float,c:str):
    """
    Parameters
    ----------
        a (int): integer number.
        b (float): description that takes
            more than 1 line in docstr
        c (str): word.
    """
    pass

def bsr(a:int,b:float,c:str):
    """
    Parameters
    ----------
        a : integer
            integer number.
        b (float): description that takes
            more than 1 line in docstr
        c (str): word.
    """
    pass

def embedded_boldings():
    """
    Default YAWNS configuration. All security constants (like keys) are undefined.

    All keys must be prefixed with `YAWNS_` because this is added to the Sanic
    object's configuration, and it can conflict with some configuration of the
    Sanic object.

    **DO NOT EDIT THIS FILE**, because it *will* be overwritten on upgrade.
    """

def seealso():
    """
    This is a paragraph.

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :ref:`howto/operator:BashOperator`

    """

def termlist_with_classifier():
    """
    See Also
    --------
    clustermap : Plot a matrix using hierarchical clustering to arrange the
                 rows and columns.
    """


def airflow_example():
    '''
    Execute a Bash script, command or set of commands.

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :ref:`howto/operator:BashOperator`

    If BaseOperator.do_xcom_push is True, the last line written to stdout
    will also be pushed to an XCom when the bash command completes

    :param bash_command: The command, set of commands or reference to a
        Bash script (must be '.sh' or '.bash') to be executed. (templated)
    :param env: If env is not None, it must be a dict that defines the
        environment variables for the new process; these are used instead
        of inheriting the current process environment, which is the default
        behavior. (templated)
    :param append_env: If False(default) uses the environment variables passed in env params
        and does not inherit the current process environment. If True, inherits the environment variables
        from current passes and then environment variable passed by the user will either update the existing
        inherited environment variables or the new variables gets appended to it
    :param output_encoding: Output encoding of Bash command
    :param skip_on_exit_code: If task exits with this exit code, leave the task
        in ``skipped`` state (default: 99). If set to ``None``, any non-zero
        exit code will be treated as a failure.
    :param cwd: Working directory to execute the command in (templated).
        If None (default), the command is run in a temporary directory.
        To use current DAG folder as the working directory,
        you might set template ``{{ dag_run.dag.folder }}``.

    Airflow will evaluate the exit code of the Bash command. In general, a non-zero exit code will result in
    task failure and zero will result in task success.
    Exit code ``99`` (or another set in ``skip_on_exit_code``)
    will throw an :class:`airflow.exceptions.AirflowSkipException`, which will leave the task in ``skipped``
    state. You can have all non-zero exit codes be treated as a failure by setting ``skip_on_exit_code=None``.

    .. list-table::
       :widths: 25 25
       :header-rows: 1

       * - Exit code
         - Behavior
       * - 0
         - success
       * - `skip_on_exit_code` (default: 99)
         - raise :class:`airflow.exceptions.AirflowSkipException`
       * - otherwise
         - raise :class:`airflow.exceptions.AirflowException`

    .. note::

        Airflow will not recognize a non-zero exit code unless the whole shell exit with a non-zero exit
        code.  This can be an issue if the non-zero exit arises from a sub-command.  The easiest way of
        addressing this is to prefix the command with ``set -e;``

        .. code-block:: python

            bash_command = "set -e; python3 script.py '{{ next_execution_date }}'"

    .. note::

        Add a space after the script name when directly calling a ``.sh`` script with the
        ``bash_command`` argument -- for example ``bash_command="my_script.sh "``.  This
        is because Airflow tries to apply load this file and process it as a Jinja template to
        it ends with ``.sh``, which will likely not be what most users want.

    .. warning::

        Care should be taken with "user" input or when using Jinja templates in the
        ``bash_command``, as this bash operator does not perform any escaping or
        sanitization of the command.

        This applies mostly to using "dag_run" conf, as that can be submitted via
        users in the Web UI. Most of the default template variables are not at
        risk.

    For example, do **not** do this:

    .. code-block:: python

        bash_task = BashOperator(
            task_id="bash_task",
            bash_command='echo "Here is the message: \'{{ dag_run.conf["message"] if dag_run else "" }}\'"',
        )

    Instead, you should pass this via the ``env`` kwarg and use double-quotes
    inside the bash_command, as below:

    .. code-block:: python

        bash_task = BashOperator(
            task_id="bash_task",
            bash_command="echo \"here is the message: '$message'\"",
            env={"message": '{{ dag_run.conf["message"] if dag_run else "" }}'},
        )

    '''

def fieldswithchildren():
    """
    Field list

    :param a: Description of a
        a longer child description

        continued on the next line
    """

def fieldswithsubchildren():
    """
    :param type\_: The column's type, indicated using an instance which
        subclasses :class:`~sqlalchemy.types.TypeEngine`.  If no arguments
        are required for the type, the class of the type can be sent
        as well, e.g.::

            # use a type with arguments
            Column('data', String(50))

            # use no arguments
            Column('level', Integer)

        The ``type`` argument may be the second positional argument
        or specified by keyword.
    """

def embedded_boldings():
    """
    Default YAWNS configuration. All security constants (like keys) are undefined.

    All keys must be prefixed with `YAWNS_` because this is added to the Sanic
    object's configuration, and it can conflict with some configuration of the
    Sanic object.

    **DO NOT EDIT THIS FILE**, because it *will* be overwritten on upgrade.
    """

def listtable():
    """
    .. list-table::
        :widths: 10 10 15
        :header-rows: 1

        * - Name
          - Type
          - Description
        * - \`\`a\`\`
          - \`\`int\`\`
          - Description of a
        * - \`\`b\`\`
          - \`\`str\`\`
          - Description of b
    """

def seealso():
    """
    This is a paragraph.

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :ref:`howto/operator:BashOperator`

    """

def termlist_with_classifier():
    """
    See Also
    --------
    clustermap : Plot a matrix using hierarchical clustering to arrange the
                 rows and columns.
    """

def airflow_example():
    """
    Execute a Bash script, command or set of commands.

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :ref:`howto/operator:BashOperator`

    If BaseOperator.do_xcom_push is True, the last line written to stdout
    will also be pushed to an XCom when the bash command completes

    :param bash_command: The command, set of commands or reference to a
        Bash script (must be '.sh' or '.bash') to be executed. (templated)
    :param env: If env is not None, it must be a dict that defines the
        environment variables for the new process; these are used instead
        of inheriting the current process environment, which is the default
        behavior. (templated)
    :param append_env: If False(default) uses the environment variables passed in env params
        and does not inherit the current process environment. If True, inherits the environment variables
        from current passes and then environment variable passed by the user will either update the existing
        inherited environment variables or the new variables gets appended to it
    :param output_encoding: Output encoding of Bash command
    :param skip_on_exit_code: If task exits with this exit code, leave the task
        in ``skipped`` state (default: 99). If set to ``None``, any non-zero
        exit code will be treated as a failure.
    :param cwd: Working directory to execute the command in (templated).
        If None (default), the command is run in a temporary directory.
        To use current DAG folder as the working directory,
        you might set template ``{{ dag_run.dag.folder }}``.

    Airflow will evaluate the exit code of the Bash command. In general, a non-zero exit code will result in
    task failure and zero will result in task success.
    Exit code ``99`` (or another set in ``skip_on_exit_code``)
    will throw an :class:`airflow.exceptions.AirflowSkipException`, which will leave the task in ``skipped``
    state. You can have all non-zero exit codes be treated as a failure by setting ``skip_on_exit_code=None``.

    .. list-table::
       :widths: 25 25
       :header-rows: 1

       * - Exit code
         - Behavior
       * - 0
         - success
       * - `skip_on_exit_code` (default: 99)
         - raise :class:`airflow.exceptions.AirflowSkipException`
       * - otherwise
         - raise :class:`airflow.exceptions.AirflowException`

    .. note::

        Airflow will not recognize a non-zero exit code unless the whole shell exit with a non-zero exit
        code.  This can be an issue if the non-zero exit arises from a sub-command.  The easiest way of
        addressing this is to prefix the command with ``set -e;``

        .. code-block:: python

            bash_command = "set -e; python3 script.py '{{ next_execution_date }}'"

    .. note::

        Add a space after the script name when directly calling a ``.sh`` script with the
        ``bash_command`` argument -- for example ``bash_command="my_script.sh "``.  This
        is because Airflow tries to apply load this file and process it as a Jinja template to
        it ends with ``.sh``, which will likely not be what most users want.

    .. warning::

        Care should be taken with "user" input or when using Jinja templates in the
        ``bash_command``, as this bash operator does not perform any escaping or
        sanitization of the command.

        This applies mostly to using "dag_run" conf, as that can be submitted via
        users in the Web UI. Most of the default template variables are not at
        risk.

    For example, do **not** do this:

    .. code-block:: python

        bash_task = BashOperator(
            task_id="bash_task",
            bash_command='echo "Here is the message: \'{{ dag_run.conf["message"] if dag_run else "" }}\'"',
        )

    Instead, you should pass this via the ``env`` kwarg and use double-quotes
    inside the bash_command, as below:

    .. code-block:: python

        bash_task = BashOperator(
            task_id="bash_task",
            bash_command="echo \"here is the message: '$message'\"",
            env={"message": '{{ dag_run.conf["message"] if dag_run else "" }}'},
        )

    """

class SimpleBleDevice(object):
    """This is a conceptual class representation of a simple BLE device
    (GATT Server). It is essentially an extended combination of the
    :class:`bluepy.btle.Peripheral` and :class:`bluepy.btle.ScanEntry` classes

    :param client: A handle to the :class:`simpleble.SimpleBleClient` client
        object that detected the device
    :type client: class:`simpleble.SimpleBleClient`
    :param addr: Device MAC address, defaults to None
    :type addr: str, optional
    :param addrType: Device address type - one of ADDR_TYPE_PUBLIC or
        ADDR_TYPE_RANDOM, defaults to ADDR_TYPE_PUBLIC
    :type addrType: str, optional
    :param iface: Bluetooth interface number (0 = /dev/hci0) used for the
        connection, defaults to 0
    :type iface: int, optional
    :param data: A list of tuples (adtype, description, value) containing the
        AD type code, human-readable description and value for all available
        advertising data items, defaults to None
    :type data: list, optional
    :param rssi: Received Signal Strength Indication for the last received
        broadcast from the device. This is an integer value measured in dB,
        where 0 dB is the maximum (theoretical) signal strength, and more
        negative numbers indicate a weaker signal, defaults to 0
    :type rssi: int, optional
    :param connectable: `True` if the device supports connections, and `False`
        otherwise (typically used for advertising ‘beacons’).,
        defaults to `False`
    :type connectable: bool, optional
    :param updateCount: Integer count of the number of advertising packets
        received from the device so far, defaults to 0
    :type updateCount: int, optional
    """

    def __init__(self, client, addr=None, addrType=None, iface=0,
                 data=None, rssi=0, connectable=False, updateCount=0):
        """Constructor method
        """
        super().__init__(deviceAddr=None, addrType=addrType, iface=iface)
        self.addr = addr
        self.addrType = addrType
        self.iface = iface
        self.rssi = rssi
        self.connectable = connectable
        self.updateCount = updateCount
        self.data = data
        self._connected = False
        self._services = []
        self._characteristics = []
        self._client = client

    def getServices(self, uuids=None):
        """Returns a list of :class:`bluepy.blte.Service` objects representing
        the services offered by the device. This will perform Bluetooth service
        discovery if this has not already been done; otherwise it will return a
        cached list of services immediately..

        :param uuids: A list of string service UUIDs to be discovered,
            defaults to None
        :type uuids: list, optional
        :return: A list of the discovered :class:`bluepy.blte.Service` objects,
            which match the provided ``uuids``
        :rtype: list On Python 3.x, this returns a dictionary view object,
            not a list
        """
        self._services = []
        if(uuids is not None):
            for uuid in uuids:
                try:
                    service = self.getServiceByUUID(uuid)
                    self.services.append(service)
                except BTLEException:
                    pass
        else:
            self._services = super().getServices()
        return self._services

    def setNotificationCallback(self, callback):
        """Set the callback function to be executed when the device sends a
        notification to the client.

        :param callback: A function handle of the form
            ``callback(client, characteristic, data)``, where ``client`` is a
            handle to the :class:`simpleble.SimpleBleClient` that invoked the
            callback, ``characteristic`` is the notified
            :class:`bluepy.blte.Characteristic` object and data is a
            `bytearray` containing the updated value. Defaults to None
        :type callback: function, optional
        """
        self.withDelegate(
            SimpleBleNotificationDelegate(
                callback,
                client=self._client
            )
        )

    def getCharacteristics(self, startHnd=1, endHnd=0xFFFF, uuids=None):
        """Returns a list containing :class:`bluepy.btle.Characteristic`
        objects for the peripheral. If no arguments are given, will return all
        characteristics. If startHnd and/or endHnd are given, the list is
        restricted to characteristics whose handles are within the given range.

        :param startHnd: Start index, defaults to 1
        :type startHnd: int, optional
        :param endHnd: End index, defaults to 0xFFFF
        :type endHnd: int, optional
        :param uuids: a list of UUID strings, defaults to None
        :type uuids: list, optional
        :return: List of returned :class:`bluepy.btle.Characteristic` objects
        :rtype: list
        """
        self._characteristics = []
        if(uuids is not None):
            for uuid in uuids:
                try:
                    characteristic = super().getCharacteristics(
                        startHnd, endHnd, uuid)[0]
                    self._characteristics.append(characteristic)
                except BTLEException:
                    pass
        else:
            self._characteristics = super().getCharacteristics(startHnd,
                                                               endHnd)
        return self._characteristics

    def connect(self):
        """Attempts to initiate a connection with the device.

        :return: `True` if connection was successful, `False` otherwise
        :rtype: bool
        """
        try:
            super().connect(self.addr,
                            addrType=self.addrType,
                            iface=self.iface)
        except BTLEException as ex:
            self._connected = False
            return (False, ex)
        self._connected = True
        return True

    def disconnect(self):
        """Drops existing connection to device
        """
        super().disconnect()
        self._connected = False

    def isConnected(self):
        """Checks to see if device is connected

        :return: `True` if connected, `False` otherwise
        :rtype: bool
        """
        return self._connected

    def printInfo(self):
        """Print info about device
        """
        print("Device %s (%s), RSSI=%d dB" %
              (self.addr, self.addrType, self.rssi))
        for (adtype, desc, value) in self.data:
            print("  %s = %s" % (desc, value))

def sphinxexample():
    """
    Sends a message
    
    :param str sender: The person sending the message
    :param str recipient: The recipient of the message
    :param message_body: The body of the message
    :type message_body: str
    :param bool urgent: True if the message is urgent, False otherwise
    :return: The time the message was sent
    :raises ValueError: If the message_body is empty
    """


def multilinetable():
    """
    ==================== =========================================================
    Compatibility
    functions - removed
    in the new API
    -------------------- ---------------------------------------------------------
    rand                 Uniformly distributed values.
    randn                Normally distributed values.
    ranf                 Uniformly distributed floating point numbers.
    random_integers      Uniformly distributed integers in a given range.
                        (deprecated, use ``integers(..., closed=True)`` instead)
    random_sample        Alias for `random_sample`
    randint              Uniformly distributed integers in a given range
    seed                 Seed the legacy random number generator.
    ==================== =========================================================
    """

def predefinedlink():
    """
    Here's an inline link to the [Python](https://www.python.org/) website.
    """

def builtins_dict():
    """
    dict() -> new empty dictionary

    dict(mapping) -> new dictionary initialized from a mapping object's
        (key, value) pairs

    dict(iterable) -> new dictionary initialized as if via:
    
        d = {}
        for k, v in iterable:
            d[k] = v

    dict(**kwargs) -> new dictionary initialized with the name=value pairs
        in the keyword argument list.  For example:  dict(one=1, two=2)
    """

def emptyterm():
    """
    Parameters
    ---------

    myparam1 : str
    myparam2 : int
    """

def modulestring():
    """
    pydocstring CLI provides entrypoints for CLI commands

    Currently only the ``pydocstring`` command is supported

    To use pydocstring from the command line you call ``pydocstring`` with the source, and optionally
    the position of the cursor within that source (defaults to the end).

    Note that pydocstring doesn't insert docstrings in place (yet), as it's designed for editor
    integration.
    It prints out the generated docstring for the scope the given cursor position is in.

    You may also want to provide the ``-f`` flag with the formatter you want to use.

    .. code-block:: text

        usage: pydocstring [-h] [-f {google,numpy,reST}] [--version] source [position]

        positional arguments:
        source                Source code to process, or the path to a file
        position              Position of the cursor in the document, defaults to
                            the end. Row, then column

        optional arguments:
        -h, --help            show this help message and exit
        -f {google,numpy,reST}, --formatter {google,numpy,reST}
                                docstring formatter to use
        --version             show program's version number and exit
    """