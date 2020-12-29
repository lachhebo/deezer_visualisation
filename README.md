# Deezer_visualisation


Data viz with your deezer data

## Cron Jobs

```sh
0 15 * * *  {PYHON_PATH}  {PROJECT_PATH}/py-music-history-visualisation/main.py history {DEEZER_TOKEN} {USER_ID} --filename={FOLDER_BACKUP}/history >> {LOGS_FILE} 2>&1

0 15 * * 1,3,5  {PYHON_PATH}  {PROJECT_PATH}/py-music-history-visualisation/main.py favorite  {DEEZER_TOKEN} {USER_ID} --filename={FOLDER_BACKUP}/favorites  >> {LOGS_FILE} 2>&1
```