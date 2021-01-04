# Low-Rate TCP-Targeted Denial of Service Attacks

This is a reproduction of [Low-Rate TCP-Targeted Denial of Service Attacks](http://www.cs.northwestern.edu/~akuzma/rice/doc/shrew.pdf).

The original code is from [https://github.com/hotpxl/low-rate-tcp-targeted-dos-attacks.git](https://github.com/hotpxl/low-rate-tcp-targeted-dos-attacks.git)

And this is the version to reproduce both Figure-4 and Figure-6 of the paper.

## Steps to reproduce
1.  Create a virtual machine with Ubuntu 16.10.

2.  In your GCE instance, execute the following:

    ```bash
    sudo apt-get update
    sudo apt-get install git
    sudo apt-get install iperf
    ```

    And 
 
    ```bash
    curl "https://cs.stanford.edu/people/rpropper/cs244/setup.sh" | /bin/bash
    ```

    This script will install Python dependencies (e.g. matplotlib), check out
    and install Mininet. Note: We provide this setup script as a separate step
    from the VM image for better clarity and transparency.  Feel free to
    inspect the script before running it.

3.  Clone our git repo:

    ```bash
    git clone https://github.com/zyainfal/EL7353_project.git
    ```

4.  Now, `cd low-rate-tcp-targeted-dos-attacks` and `sudo ./run_all.sh` to run the
    experiment. Please be patient; a run takes around 30 hours.Run `sudo ./run.sh` 
    if you only want to run single TCP test or `sudo run.sh -f`, the 5 aggregated 
    TCP throughput test. Each test may take 15 hours.

5.  After the script runs, there should be two generated `.png` files in the root 
    directory. One (`results-<hostname>-date_rate.png`) will show the normalized
    throughput, i.e., the figures we are trying to reproduce.

