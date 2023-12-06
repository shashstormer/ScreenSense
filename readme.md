# ScreenSense

## What is this?

This is a simple script that tracks your usage across all your apps on windows.

### If you run into any issues while installing requirements, try using python 3.6.x
## How to use?

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Optional (If you wish to use a specific python environment) you must edit the `run_dasboard_server.bat` and `track_usage_activity.bat` and activate the environment/change python location before running the script.
4. #### Create a shortcut of `usage_activity_tracker_activate.bat` and place it in the startup folder at C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.
   1. This will ensure that the script runs everytime you start your computer.
   2. #### remember to replace `{user}` with your actual username according to your pc.
5. You can now check your usage at http://localhost:5003/


## Planned:
1. Improve browser tracking using a browser extension and api.
   > 1. Add domain wise tracking for browsers.
2. Improve Dashboard
   > 1. Add graphs, charts, etc
   > 
   > 2. Improve UI
   > 
   > 3. Add features to allow advanced analysis of data on the dashboard.

3. Improve data aggregating system
   > 1. Collect more data
   > 2. Improve the way data is stored (format of data, using more data like times the app was in use).
   > 3. Aggregate data better to allow for more advanced analysis.


### If you have any questions, suggestions, bug reports, or feature requests feel free to contact me at:  
> Email: [shashanka5398@gmail.com](mailto:shashanka5398@gmail.com) (avoid)
> 
> Discord: [shashstorm's server](https://discord.gg/CgDsUGAKtA) (preferred)

### I prefer you contact through discord for any issues or suggestions or requests or bug reports.
You can always create an issue on github if you are not comfortable with discord.
