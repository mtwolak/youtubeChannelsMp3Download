# Youtube video downloader
Simple program to download videos from youtube's channels from specified date.

## Requirements
- Unix system
- Python 3
- Installed youtube-dl
- Developer google key
## Example configuration
Settings.json must be filled with configuration.
For each channel following tags are required:
- name or id
- folderName where music will be downloaded
```
{
  "settings": {
    "startDate": "2018-11-21",
    "developerKey": "AIzaSyFeYTsPtfrCQExovAib9pjLM55i8_z6UuB"
  },
  "channels": [
    {
      "name": "AllTrapNation",
      "folderName": "TrapNation"
    },
    {
      "id": "UCj_Y-xJ2DRDGP4ilfzplCOQ",
      "folderName": "HouseNation",
      "_comment": "House nation"
    }
  ]
}
```