# Ask for point in time to recover with TSM.
# One point in time is used for all filespaces.

LogPrint ""
LogPrint "Galaxy10 restores by default the latest backup data. Alternatively you can specify"
LogPrint "a different date and time to enable Point-In-Time Restore. Press ENTER to"
LogPrint "use the most recent available backup"
read -t $WAIT_SECS -r -p "Enter date/time (MM/DD/YYYY HH:mm:ss) or press ENTER [$WAIT_SECS secs]: " 2>&1
# validate input
if test -z "${REPLY}"; then
    LogPrint "Skipping Point-In-Time Restore, will restore most recent data."
    GALAXY10_PIT=""
    GALAXY10_ZEIT=""
else
    # validate date
	
    GALAXY10_ZEIT=$REPLY
    GALAXY10_PIT="QR_RECOVER_POINT_IN_TIME"

fi

