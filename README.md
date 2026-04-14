# Idea

make a way to suspend when system on battery and auto awake with calculated delay based on remaining battery to check batery level and then hibernate to save progress 
at a critical range between 10-5%.

## Whats done 

The delay calculation ,battery state and level detection ,root gui dialogue display resolved, 
yad dialogue and countdown,to detect whether it was a manual or rtcwake , to run a repeated check when system wakes from the suspend.

##  Whats left (additional,script works now)

- Check Big(O) worst case time. should not exceed 15sec +- 2(old calculation but still a good/safe target) for timer service and script avoid overlap race conditions
- considering usage of a fifo or other make lock functions though seems unnecessary currently.
- when the delay is above 3-4 hrs/discharging cap it at 3/4 hrs till delay comes down mentioned time
- remove upower dependency (refresh_values) with pure arithmetic instead and subsequently other dependencies (if evident advantages (Prefer low latency coreutils) and optionally support lower bash versions)
- avoid polling with very small intervals to 
avoid overhead or countinuos looping , avoid race conditions when 
tampering system files as very short wakeup for check time can cause 
same delay to be reused (maybe upower quirk )
- avoid systemd timer if possible and replace with a low memory latency polling method
- ~~find a secure way to run suspend wrapper for all users without escalating priviledges(use suspend-then-hibernate hibernatedelaysec ?)~~ 
- remove systemd suspend calls with rtcwake commands if needed
- find any interference with long running processes or hanged situations (bigger delay)
- an indication that the suspend loop was completed and battery has reached critical levels and hibernated (for info only no utility use as of now) 
- touch the LOCK file with random names(using mktemp?)
- need checking for deps all time or store it in the lock file (what if one of the becomes unavailable during suspends?Possible?)
- error handling when hibernate fails from OS's side (not critical now as lockfile is removed then,but data loss after battery drain to death)
---
- Zramswap has caused page allocation issues during hibernate in systemd systems.
---
## Usage

- copy the main script to the location specified on the systemd service file (current timer method [systemd-timer])
- install the timer and the service file and enable them as systemd root 
- run script in terminal or make a keybind for ease

## Testing
- A simulation folder has a dummy sysfs cp to /tmp or any dir, make a copy of main script, edit prefix of the sysfs detection for loop with your dir
then echo in your values to test various battery conditions

### --potential bottlenecks/errors--


**1**.upower query when slow (0.5- 3.0 sec) advisable to switch method to pure arithmetic or faster coreutil & upower not updating power properly (need check)

**2**.delays in battery_action: 

- reduce yad dialogue or increase timer to 30 sec

- systemctl hibernate may take upto 30 sec .timer job has to be stopped within the repeat range we get a worst case of 5(init_setup)+10(dialogue)=15 sec.
so the first 5 sec need to terminate the timer job or increase timer to 30 sec

- calling of battery_action in s3_detect (battery_action may have a 40 sec worst case)

- a potential crash can persist the lockfile (unlikely as the next timer job should kill it or no? need verification) (also countinues crashes will cause a loop)
(also systems not using tmpfs for tmp or clears temp at reboot cause issue)

- systemctl hibernate -i &&  rm -f /tmp/sulockfile && exit 0 here what if hibernte fails but lockfiles removed? how does this work need help

**3**.X Authority Detection logic ,have noticed missing dialogues in multi-user need fix~~
- yad dialogues dont show at times but still the work after it is done,~~(declare xauth detection as a function and call just before yad display?)~~

**4**.~~add a recursion counter for the s3_detect call (help needed whether its necessary)~~

**5**.~~CRITICAL s3wrapper need  root or temporarily escalate privilages (sudo) due to rtcwake command (help needed:potential solutions ..)~~
- ~~adding NOPASSWD for wrapper in sudoers ,but not appealing security-wise (sudo only systems)~~
- ~~setuid bit (means hardening of wrapper required)(info only dont use)~~
- ~~polkit rule for rtcwake commmand for users group(preferred for now but complex setup~~
- ~~give cap_dac_override capability (very risky if the binary is compromised)~~

~~Hardening steps(for cap_dac_override permission)~~
--- 
- ~~no write acess to binary (chmod 555) (do this first before immutable lock)~~ 
- ~~immutable lock flag (chattr +i /binary,-i for reversing) (remove the lock during updates [package:linux-util(systemcore package)])~~
---
- ~~Using pkexec - each wrapper call asks for a polkit auth (enter password dialogue) which elevates to root one run. (Current method,Comparitively secure).~~

**6**.An almost 12 hour suspend starting at approx 95% charge test has failed with failure to countinue suspend check due to early clearence of lock file 
potential cause was found in battery_check and rectified but the timer method may also prove to be unreliable. (need testing)

**7**.~~How to deal(cancel suspend) between the wrapper timeout till the timer catches up and starts the s3_detect loop.~~

**8**.Race Condition where one timer triggered script runs the yad dialogue then the timer triggers another dialogue after interval.(not observed just a possibility to mitigate)(add a pid check?)
