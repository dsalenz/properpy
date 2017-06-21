# properpy

This script is based on python3. 
It currently only runs on Linux and MacOS since it uses grep as a maincomponent.

LOGIC
1. The script loads all property keys out of all files for one local into one list.
2. Then it runs through the list and checks for each key if it is referenced in the code. It is searching in all files of the project but excludes property files.
3. While the script is running there is a commandline-output where you can see what file is currently checked. There is also an output if the script finds a unreferenced key.
4. All unreferenced keys will be written into a logfile. The location of the logfile can be set with a variable inside the script.
5. After the script checked all keys for one local it will do the same for all other locals set in the variable inside the script.



In the future I wil make this script more generic so it is easier to use and setup and also easier to reuse for other projects. But at first I will refactor it 
 

