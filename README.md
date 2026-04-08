# PLAN

make a way to suspend when system on battery and auto awake with calculated delay based on remaining battery to check batery level and then hibernate to save progress 
at a critical range between 10-5%.

## Whats done 

The delay calculation ,battery state and level detection , root gui dialogue display resolved, 
yad dialogue and countdown.


##  Whats left 

to detect whether it was a manual or rtcwake , to run a repeated check when system wakes from the suspend 

### Potential clues

rtcwake command can do a s3 or s4 state with a RTC clock which runs in both modes and can trigger a wake
currently systemd commands are used and are in thought to be changed

## Usage
copy the main script and s3 wrapper to the location specified on the systemd service file (current timer methodology)
install the timer and the service file and run them as systemd root 
the intervals can be tuned which works best for you

#### additional

Prefer low latency coreutils , reduce additional dependencies (yet optionally use common installed utils if needed) ,
avoid polling with very small intervals to avoid overhead or countinuos looping , avoid race conditions when tampering system files 
very short wakeup for check time can cause same delay to be reused (maybe upower quirk )
