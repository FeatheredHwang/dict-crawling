# anki-myaddon

This is my template of Anki add-on developing.








## Setting up a development environment

### IDE
The free community edition of PyCharm has good out of the box support for Python: https://www.jetbrains.com/pycharm/. You can also use other editors like Visual Studio Code.

After installation of PyCharm completed, setup `External Tools`:

1. File>Settings>Tools>External Tools

2. `Qt Designer`

   > It will pop up error window until you install the required dependency (pyqt5-tools) in your venv.

   - Program  - 
     In Windows: `$ProjectFileDir$\.venv\Lib\site-packages\pyqt5_tools\Qt\bin\designer.exe`
     In Linux: `$ProjectFileDir$/.venv/lib/python3.8/site-packages/pyqt5_tools/Qt/bin/designer`

   - Arguments -  `$FilePath$`
   - Working Directory -  `$ProjectFileDir$`

3. `PyUIC`

   - Program - 
     In Windows: `$ProjectFileDir$\.venv\Scripts\pyuic5.exe`
     In Linux: `/usr/bin/pyuic5`
   - Arguments - `$FileName$ -o $FileNameWithoutExtension$.py`
   - Working Directory - `$FileDir$`.

### Repository

Please note that we use Python 3 only, so make sure that you use correct version when running commands below.

1. First, clone the repository, step into newly created directory.

2. Create a new virtual environment:

   ```
   # macOS/Linux
   # You may need to run sudo apt-get install python3-venv first
   python3 -m venv .venv

   # Windows
   # You can also use py -3 -m venv .venv
   python -m venv .venv
   ```

3. Activate virtual environment:

   ```
   # macOS/Linux
   source .venv/bin/activate
   # This script is written for the bash shell. If you use the **csh** or **fish** shells,
   # there are alternate `activate.csh` and `activate.fish` scripts you should use instead.

   # Windows
   # Pycharm
   .venv\Scripts\activate.bat
   # VSCode
   .venv\Scripts\activate.ps1
   ```

4. Configure Project Interpreter in Pycharm settings > Project > Project Interpreter

5. Update pip:

   ```
   pip -V
   pip install --upgrade pip
   ```

6. Then, install all the required dependencies:

   ```
   pip install -r requirements.txt
   ```

