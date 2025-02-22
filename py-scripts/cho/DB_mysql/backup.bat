@echo off
set DB_NAME=third_project
set DB_USER=cho
set BACKUP_PATH=C:\Users\MYCOM\Desktop
set FILE_NAME=%BACKUP_PATH%\%DB_NAME%_backupData_%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%.sql

mysqldump -u %DB_USER% -p -h 192.168.0.184 %DB_NAME% > "%FILE_NAME%"
echo Backup completed: %FILE_NAME%
pause