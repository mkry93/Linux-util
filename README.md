# PLAN

make a way to suspend when system on battery and auto awake with calculated delay based on remaining battery to check batery level and then hibernate to save progress 
at a critical range between 10-5%.

## Whats done 

The delay calculation ,battery state and level detection , root gui dialogue display resolved, 
yad dialogue and countdown.


##  Whats left 

to detect whether it was a manual or rtcwake , to run a repeated check when system wakes from the suspend 

#### Potential clues

rtcwake command can do a s3 or s4 state with a RTC clock which runs in both modes and can trigger a wake
currently systemd commands are used and are in thought to be changed

## Usage

copy the main script and s3 wrapper to the location specified on the systemd service file (current timer methodology)
install the timer and the service file and run them as systemd root 
the intervals can be tuned which works best for you

## additional

Prefer low latency coreutils , reduce additional dependencies (yet optionally use common installed utils if needed) ,
avoid polling with very small intervals to avoid overhead or countinuos looping , avoid race conditions when tampering system files 
very short wakeup for check time can cause same delay to be reused (maybe upower quirk )

Check Big(O) worst case time. should not exceed 15sec +- 2

- A simulation folder has a dummy sysfs cp to /tmp or any dir, make a copy of main script, edit prefix of the sysfs detection for loop with your dir
then echo your values to test various battery conditions

### potential bottlenecks
---
1.upower query when slow (.5- 3.0 sec) advisable to switch method to pure arithmetic or faster coreutil

2.delays in battery_action: 

a.reduce yad dialogue or increase timer to 30 sec

b.systemctl hibernate may take upto 30 sec .timer job has to be stopped within the repeat range we get a worst case of 5(init_setup)+10(dialogue)=15 sec.
so the first 5 sec need to terminate the timer job or increase timer to 30 sec

c.calling of battery_action in s3_detect (battery_action may have a 40 sec worst case)

d.a potential crash can persist the lockfile (unlikely as the next timer job should kill it or no? need verification) (also countinues crashes will cause a loop)
(also systems not using tmpfs for tmp or clears temp at reboot cause issue)

e.systemctl hibernate -i &&  rm -f /tmp/sulockfile && exit 0 here what if hibernte fails but lockfiles removed? how does this work need help

3.X Authority Detection have noticed missing dialogues in multi-user need fix

4.add a recursion counter for the s3_detect call (help needed whether its necessary)

5.for practical reasons is it necessary to add a max 3-4 hour check if exceeding at worst condition(100%) the delay would be ~16 hours

6.CRITICAL for s3wrapper to work either run as root or temporarily escalate 
priviledge (sudo) due to rtcwake command (help needed:potential solution is adding NOPASSWD for rtcwake in sudoers ,but not appealing security-wise )
