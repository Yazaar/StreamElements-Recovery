# StreamElements Data Recovery

### Recover data which got lost during the backup failure

All data that was registered between 4:th November 2019 and 24:th Febuary 2020 at StreamElements got lost which is why I developed this tool to extract data from Twitch's existing chat history. You can find a step by step guide right underneath this, but I would recommend to scroll down and read the risks, for your own safety.

**Warning: I take no responsibility for the outcome!**

#### This is how it works:

1. A user with moderator privileges or higher heads over to the channel to recover
2. Types "/user StreamElements" (capitalization does not matter) to open up the bots profile
3. Clicks on the messages tab
4. Scroll up until plenty of messages are loaded, the current date should be written. Make sure this is 4:th of November 2019 but preferably earlier for less future work
5. Rightclick a message, or anything really, click "inspect". Or use a keyboard shortcut (F12) (CTRL + SHIFT + I)
6. Click "Console" found close to the top
7. Paste the following, all messages should get marked: "document.querySelector('.message').parentElement.parentElement.innerHTML"
8. Hit enter and scroll all of the way to the right, then hit copy
9. Open "parseme.txt", Paste and save
10. Find the date where the data loss occurred (2/24/2020) and find the following \<div class="tw-align-items-center tw-flex"\>, should be found about 136‬ letters to the left, from the start of that remove EVERYTHING underneath. Then save. (the messy part is over, well done)
11. Go to StreamElements website and then to your channel settings (click your name top left and then settings)
12. Copy the "Account ID" and paste it in the file called "SE_userid.txt"
13. Optional but open feel free to open up "points-per-minute.txt" and insert the amount of points users get per minute watched. **I prefer to edit this manually to get more accurate results, which means that I leave this text file alone**
14. Run the python file or the windows executable ("extractor.exe" or "extractor.py"), if you run the python file install the dependencies (requests, lxml, bs4)
15. 3 valuable files should get generated: "result-only-watchtime.csv", "result-complete.csv", "result-only-points.csv" and the process is pretty much finished
    "result-complete.csv" contains ready to import data with both watchtimes and points.
    "result-only-points.csv" contains ready to import data, but no watchtimes will get modified since those users was not found in the chat history.
    "result-only-watchtime.csv" contains data which has to be edited manually, unless if you specified a number in "points-per-minute.txt" but this is usually not accurate (look it through if you care about points) (**I looked through all three...**)
    **data structure:**
    "username,twitchID,currentPoints,alltimePoints,watchtime"
    username: Twitch username
    twitchID: Always empty
    currentPoints: How much points the user has
    alltimePoints: Yeah, highest points of all time
    watchtime: User's watchtime in minutes
16. When you are happy with the files head over to the StreamElements website, should find a import top right. Click it and then on "other" and finally click "Import from CSV". Select all three files and you should be restored, not perfect but better than before. The files will overwrite the data for the user which means that you can create a CSV file yourself to modify watchtimes (points can be changed on the website, recommended)
17. Happy Streaming
    // Yazaar

#### Risks

There are no risks to perform the extraction process but the moment you upload the files ti their site it is irreversible, unless if you upload a modified file since all imports overwrites the specified users completly (unless if the "column" is blank like following: "username,twitchID,currentPoints,alltimePoints,", that but with real values would leave watchtime unchanged)

Not all users will benefit from this extraction process since it requires a response which exposes their watchtime or points values.

Some users might lose points if the script is unable to find their current value (will leave it blank for you to specify or calculate depending on their watchtime). But this is only a problem if watchtime is exposed and not their points, if none of them are will their current record from 4:th November be unchanged (watchtime and points)

I take **no responsibility** for the outcome but would recommend this method (used it myself on multiple channels but I read all files manually)
