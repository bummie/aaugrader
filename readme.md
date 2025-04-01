# Syscall Graph Detection Testing POC

## Create output from strace
```sh
strace -fvy -s 256 ./aaugrader 2> src/detection/samples/magdan21.strace
```

## Usage detection tool

Source virtual env
```sh
# Craete virtual env
python3 -m venv venv

# Install required dependencies
pip3 install -R ./requirements.txt

# Source virtual env
. venv/bin/activate.fish

# Cat strace output and pipe it to the detection python script
# use -o / --output if you want to give the ouput a name, results are stored in /tmp/<output_name>.json/png
cat src/detection/samples/sberge24.strace | src/detection/main.py -o sberge24
```

## Ideas

### Summary of syscall
Hacker Point system.

Summarize the amount of each syscall.
Use the average of different valid runs. Use the result as a baseline,
if the current run of the binary is too far off the base average, flag as strange behaviour.

If syscall not in the average run is popping up, OR 
If the syscall amount is greater should weigh more than if they count is lower.
User might have quit the application earlier, but more syscalls would point towards long usage or hacker hacking.

Special detection if files are being read, written to. Parse file names and give hacker points if a files that usually is never opened is opened.

### Look at the ordering of different syscalls per process
 * This will be more difficult and less reliable I believe. It would be
quite interesting if it would work out.


