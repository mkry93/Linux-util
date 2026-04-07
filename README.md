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



