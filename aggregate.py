import os
import json
from datetime import datetime
from config import usage_data_folder, aggregate_data_folder, exclude_from_total_time


def aggregate_and_summarize_usage_data():
    aggregated_data = {}
    for filename in os.listdir(usage_data_folder):
        file_path = os.path.join(usage_data_folder, filename)
        if os.path.isfile(file_path) and filename.endswith(".json"):
            with open(file_path, 'r') as file:
                daily_data = json.load(file)
            date_str = filename.split(".")[0]
            date = datetime.strptime(date_str, "%d-%m-%Y").date()
            year = date.year
            month = date.strftime('%m')
            date_of_month = date.day
            if year not in aggregated_data:
                aggregated_data[year] = {"total_time": 0, "time_categories": {}, "month": {}}
            if month not in aggregated_data[year]["month"]:
                aggregated_data[year]["month"][month] = {"total_time": 0, "time_categories": {}, "day": {}}
            if date_of_month not in aggregated_data[year]["month"][month]["day"]:
                aggregated_data[year]["month"][month]["day"][date_of_month] = {"total_time": 0, "time_categories": {},
                                                                               "usage": {}}
            aggregated_data[year]["month"][month]["day"][date_of_month]["usage"].update(daily_data)
    for year in aggregated_data:
        for month in aggregated_data[year]["month"]:
            for date_of_month in aggregated_data[year]["month"][month]["day"]:
                aggregated_data[year]["month"][month]["day"][date_of_month] = aggregate_day_data(
                    aggregated_data[year]["month"][month]["day"][date_of_month])
            aggregated_data[year]["month"][month] = aggregate_month_or_year_data(
                aggregated_data[year]["month"][month])
    aggregated_data[year] = aggregate_month_or_year_data(aggregated_data[year])
    return aggregated_data


def aggregate_day_data(day_data):
    aggregated_data = {'total_time': 0, 'time_categories': {}, 'usage': {}}
    for app in day_data["usage"]:
        app_type = get_app_type(app)
        if app_type not in aggregated_data["time_categories"]:
            aggregated_data["time_categories"][app_type] = 0
            aggregated_data["usage"][app_type] = {
                app: {"total_time": sum(list(day_data["usage"][app].values())), "details": day_data["usage"][app]}
            }
        else:
            aggregated_data["usage"][app_type][app] = {"total_time": sum(list(day_data["usage"][app].values())),
                                                       "details": day_data["usage"][app]}
        if app in exclude_from_total_time:
            continue
        aggregated_data["time_categories"][app_type] += sum(list(day_data["usage"][app].values()))
    aggregated_data["total_time"] += sum(list(aggregated_data["time_categories"].values()))
    return aggregated_data


def aggregate_month_or_year_data(month_or_year_data):
    aggregated_data = month_or_year_data.copy()
    day_or_month = "month" if "month" in aggregated_data else "day"
    for day in month_or_year_data[day_or_month]:
        aggregated_data["total_time"] += month_or_year_data[day_or_month][day]["total_time"]
        for app_type in month_or_year_data[day_or_month][day]["time_categories"]:
            if app_type not in aggregated_data["time_categories"]:
                aggregated_data["time_categories"][app_type] = 0
            aggregated_data["time_categories"][app_type] += month_or_year_data[day_or_month][day]["time_categories"][
                app_type]
    return aggregated_data


def get_app_type(app_name):
    development_apps = ["pycharm", "vscode", "sublime", "eclipse", "intellij", "atom", "netbeans", "visual studio",
                        "android studio", "xcode", "code::blocks", "emacs", "jupyter", "notepad++", "rider", "brackets",
                        "phpstorm", "rubymine", "webstorm", "textmate", "vim", "gedit", "geany", "bluej", "codepen",
                        "cloud9", "glitch", "kate", "nano", "pluma", "codeanywhere", "replit", "thonny", "spyder",
                        "eric", "wing", "pydev", "anaconda", "julia", "qt creator", "kdevelop", "gephi", "lighttable",
                        "gedit", "bluefish", "komodo", "jedit", "ultraedit", "notepad2", "notepad3", "medit", "kwrite",
                        "featherpad", "scite", "textadept"]
    ide_apps = ["pycharm", "vscode", "sublime", "eclipse", "intellij", "atom", "netbeans", "visual studio",
                "android studio", "xcode", "code::blocks", "emacs", "jupyter", "notepad++", "rider", "brackets",
                "phpstorm", "rubymine", "webstorm", "textmate", "vim", "gedit", "geany", "bluej", "codepen", "cloud9",
                "glitch", "kate", "nano", "pluma", "codeanywhere", "replit", "thonny", "spyder", "eric", "wing",
                "pydev", "anaconda", "julia", "qt creator", "kdevelop", "gephi", "lighttable", "gedit", "bluefish",
                "komodo", "jedit", "ultraedit", "notepad2", "notepad3", "medit", "kwrite", "featherpad", "scite",
                "textadept"]
    gaming_apps = ["steam", "origin", "epic games", "minecraft", "fortnite", "league of legends", "dota 2", "cs:go",
                   "pubg", "overwatch", "world of warcraft", "fall guys", "apex legends", "valorant", "gta v",
                   "red dead redemption 2", "the witcher 3", "cyberpunk 2077", "destiny 2", "rainbow six siege",
                   "rocket league", "fifa", "nba 2k", "madden nfl", "assassin's creed", "doom eternal", "borderlands 3",
                   "dark souls", "god of war", "final fantasy", "kingdom hearts", "resident evil",
                   "star wars jedi: fallen order", "call of duty: warzone", "battlefield v", "far cry", "borderlands",
                   "monster hunter: world", "nintendo switch", "playstation", "xbox", "stardew valley", "terraria",
                   "subnautica", "among us", "phasmophobia", "valheim", "animal crossing", "the sims",
                   "minecraft dungeons", "diablo iii", "path of exile", "torchlight ii", "grim dawn", "epicgameslauncher", "riotgames"]
    meeting_apps = ["zoom", "teams", "skype", "google meet", "webex", "slack", "gotomeeting", "join.me",
                    "fuze", "bluejeans", "appear.in", "jitsi", "vsee", "appear.in", "cisco webex", "starleaf", "8x8",
                    "ringcentral", "zoom rooms", "lifesize", "microsoft teams", "google hangouts", "flock",
                    "bigbluebutton", "teamviewer", "anydesk", "chrome remote desktop", "logmein", "splashtop",
                    "whereby", "zoho meeting", "freeconferencecall", "skype for business", "blizz", "zoominfo",
                    "goconnect", "eztalks", "webinarjam", "workplace by facebook", "freespee", "bluejeans meetings",
                    "remo", "airmeet", "meetsocial", "houseparty", "hopin", "clinchpad", "infosuite", "meetupcall",
                    "8x8 video meetings", "screenleap", "zipwire", "daily.co", "hitchhiker"]
    streaming_apps = ["netflix", "youtube", "twitch", "hulu", "amazon prime", "disney+", "hbo max", "apple tv+",
                      "peacock", "hbo go", "spotify", "apple music", "amazon music", "pandora", "tidal", "deezer",
                      "google play music", "soundcloud", "vimeo", "dailymotion", "tiktok", "instagram live",
                      "periscope", "facebook live", "mixer", "cbs all access", "nbc", "abc", "cnn", "bbc iplayer",
                      "espn+", "hgtv", "history channel", "food network", "national geographic", "travel channel",
                      "discovery channel", "syfy", "a&e", "lifetime", "hallmark channel", "cartoon network",
                      "nickelodeon", "discovery+", "quibi", "vrv", "crunchyroll", "funimation", "hulu live", "sling tv",
                      "youtube tv", "fubo tv", "directv now", "playstation vue", "apple tv", "roku", "firestick"]
    communication_apps = ["whatsapp", "messenger", "telegram", "signal", "wechat", "line", "viber", "kakao talk",
                          "snapchat", "instagram", "twitter", "facebook", "linkedin", "tiktok", "discord", "skype",
                          "google duo", "zoom", "teams", "slack", "telegram", "threema", "voxer", "firechat",
                          "snapseed", "hangouts", "badoo", "meetme", "okcupid", "hinge", "tinder", "grindr",
                          "bumble", "coffeemeetsbagel", "match.com", "eharmony", "zoosk", "okcupid", "badoo",
                          "plenty of fish", "happn", "clover", "jack'd", "scruff", "blued", "grizzly", "surge", "romeo",
                          "gaydar", "hornet", "chappy", "bender", "squirt", "adam4adam", "manhunt", "growlr", "mr x",
                          "sturb"]
    design_apps = ["photoshop", "illustrator", "indesign", "xd", "sketch", "figma", "invision", "zeplin", "canva",
                   "gimp", "coreldraw", "affinity designer", "lunacy", "gravit designer", "adobe spark", "procreate",
                   "autodesk sketchbook", "corel painter", "krita", "clip studio paint", "paint tool sai",
                   "medibang paint", "firealpaca", "ibis paint", "comic draw", "assembly", "vectr", "skedio", "skencil",
                   "fatpaint", "sumopaint", "autodesk fusion 360", "solidworks", "rhinoceros 3d", "blender", "autocad",
                   "revit", "catia", "sketchup", "3ds max", "maya", "zbrush", "mudbox", "substance painter",
                   "quixel mixer", "marvelous designer", "gravity sketch", "c4d", "keyshot", "v-ray", "arnold",
                   "corona renderer", "octane render", "redshift", "unreal engine", "unity"]
    productivity_apps = ["microsoft office", "google workspace", "trello", "asana", "notion", "evernote", "onenote",
                         "todoist", "wunderlist", "any.do", "omnifocus", "things", "habitica", "forest", "pomodone",
                         "rescuetime", "toggl", "remember the milk", "habitbull", "focus@will", "stayfocusd",
                         "cold turkey", "freedom", "leechblock", "serene", "loop", "ticktick", "swipes", "nirvana",
                         "zenkit", "quip", "airtable", "basecamp", "zoho projects", "jira", "slack",
                         "microsoft teams", "zoom", "google meet", "skype", "toggl plan", "monday.com", "clickup",
                         "hive", "redbooth", "podio", "workfront", "smart sheets", "dapulse", "confluence", "flow"]
    finance_apps = ["mint", "ynab", "quicken", "personal capital", "wallet", "goodbudget", "everydollar", "pocketguard",
                    "expensify", "receipts by wave", "wally", "mvelopes", "simple", "chime", "acorns", "robinhood",
                    "stash", "betterment", "wealthfront", "sofi invest", "etrade", "fidelity", "schwab",
                    "td ameritrade", "ally invest", "m1 finance", "charles schwab", "vanguard", "rakuten", "ibotta",
                    "honey", "ebates", "citi", "chase", "bank of america", "wells fargo", "us bank", "capital one",
                    "discover", "american express", "barclaycard", "citizens bank", "suntrust bank", "bb&t", "pnc bank",
                    "hsbc", "regions bank", "santander", "keybank", "ally bank", "union bank", "fifth third bank",
                    "citibank", "usaa", "capital one 360", "simple bank", "chime", "sofi money", "varo", "n26", "monzo",
                    "revolut", "cash app", "venmo", "paypal", "google pay", "apple pay", "samsung pay", "square",
                    "stripe", "skrill", "neteller", "circle pay", "zelle", "western union", "moneygram", "transferwise",
                    "wise", "payoneer", "worldremit", "remitly", "ofx", "paysera", "paytm", "uphold", "airtm", "skrill",
                    "ecoPayz", "paysafecard", "webmoney", "perfect money", "neteller", "advcash", "qiwi",
                    "yandex money", "alipay", "wechat pay", "unionpay", "tenpay", "jd pay", "baidu wallet", "paytm",
                    "phonepe", "gpay", "amazon pay", "freecharge", "mobikwik", "oxigen wallet", "itau", "bradesco",
                    "santander", "caixa", "bancolombia", "davivienda", "banco de bogota", "bbva", "banesco",
                    "mercadopago", "sodexo", "edenred", "ticket restaurant", "ticket alimentacao", "alelo",
                    "vr alimentacao", "hipercard", "elo", "sodexo", "cheque comida", "cheque restaurante",
                    "cheque alimentacao"]
    health_and_fitness_apps = ["myfitnesspal", "fitbit", "strava", "runkeeper", "mapmyrun", "couch to 5k",
                               "stronglifts 5x5", "7 minute workout", "calm", "headspace",
                               "meditation studio", "daily yoga", "yoga studio"]
    news_and_magazines_apps = ["google news", "apple news", "flipboard", "smartnews", "feedly", "inoreader", "pocket",
                               "instapaper", "mozilla pocket", "readability", "nuzzel", "taptu", "pulse", "news360",
                               "circa", "yahoo news", "bbc news", "cnn", "fox news", "msnbc", "npr",
                               "the new york times", "the washington post", "the wall street journal", "usa today",
                               "associated press", "reuters", "bloomberg", "business insider", "forbes", "fortune",
                               "inc.", "fast company", "wired", "techcrunch", "mashable", "buzzfeed", "vice",
                               "huffpost", "the atlantic", "time", "national geographic", "people", "vogue",
                               "cosmopolitan", "esquire", "gq", "rolling stone", "billboard", "variety",
                               "hollywood reporter", "vanity fair", "new york magazine", "the economist",
                               "scientific american", "national geographic", "discover", "popular science", "wired",
                               "national review", "the new yorker", "slate", "the onion", "the guardian", "al jazeera",
                               "recode", "engadget", "the verge", "arstechnica", "slashdot", "gizmodo"]
    social_media_apps = ["facebook", "instagram", "twitter", "linkedin", "snapchat", "tiktok", "discord", "pinterest", "reddit",
                         "tumblr", "flickr", "vine", "youtube", "vimeo", "dailymotion", "periscope", "meerkat",
                         "ustream", "livestream", "bigo live", "facebook gaming", "youtube gaming",
                         "twitch", "smashcast", ]
    # "dlive", "caffeine", "trovo", "streamyard", "restream", "omlet arcade",
    # "mobcrush", "player.me", "mirrativ", "airshou", "az screen recorder", "mobizen", "du recorder",
    # "screenflow", "camtasia", "obs studio", "streamlabs", "xsplit", "elgato", "logitech",
    # "avermedia", "rode", "blue yeti", "audio-technica", "shure", "sennheiser", "hyperx",
    # "steelseries", "corsair", "razer", "logitech", "asus", "msi", "acer", "dell", "hp", "lenovo",
    # "apple", "samsung", "sony", "lg", "vizio", "sharp", "panasonic", "philips", "toshiba",
    # "hisense", "hitachi", "jvc", "element", "sceptre", "westinghouse", "seiki", "tcl", "insignia",
    travel_apps = ["google maps", "waze", "apple maps", "maps.me", "sygic", "here wego", "citymapper", "moovit",
                   "transit", "uber", "lyft", "grab", "gojek", "ola", "blablacar", "car2go", "zipcar", "turo",
                   "getaround", "avis", "hertz", "enterprise", "national car rental", "budget", "thrifty", "sixt",
                   "alamo", "didi", "cabs", "easy taxi", "cabify", "99taxis", "mytaxi", "beat", "careem", "gojek",
                   "pathao", "ride", "transport", "navigo", "vivarelli", "moreapp", "trackway", "getafish", "capptur",
                   "cab dash", "ride the city", "taxi pal", "cabify", "cabubble", "fareye", "holla", "cargotel",
                   "cabify", "ubercab", "lyft", "gett", "cabify", "hailo", "sidecar", "wheely", "cabby", "curb",
                   "flywheel", "bolt", "easy taxi", "le cab", "fasten", "kakao taxi", "via", "yandex.taxi", "careem",
                   "grabtaxi", "go car", "ez taxi", "indriver", "ztrip", "get taxi", "ridescout", "ridepal", "sherut",
                   "carmel", "supershuttle", "gocatch", "shebah", "blacklane", "mytaxi", "99taxis", "easy taxi",
                   "safer", "city taxi", "ridester", "trip", "mycar", "loop", "whisk", "fasten", "gig"]
    food_and_drink_apps = ["ubereats", "doordash", "grubhub", "postmates", "caviar", "eat24", "delivery.com", "goPuff",
                           "seamless", "just eat", "skipthedishes", "foodpanda", "zomato", "swiggy", "ubereats",
                           "doordash", "grubhub", "postmates", "caviar", "eat24", "delivery.com", "goPuff", "seamless",
                           "just eat", "skipthedishes", "foodpanda", "zomato", "swiggy", "starbucks", "dunkin' donuts",
                           "mcdonald's", "burger king", "wendy's", "kfc", "subway", "domino's pizza", "papa john's",
                           "pizza hut", "chipotle", "taco bell", "starbucks", "dunkin' donuts", "mcdonald's",
                           "burger king", "wendy's", "kfc", "subway", "domino's pizza", "papa john's", "pizza hut",
                           "chipotle", "taco bell", "panera bread", "sonic drive-in", "arby's", "jimmy john's",
                           "five guys", "shake shack", "inandout", "whataburger", "white castle", "culver's",
                           "raising cane's", "chick-fil-a", "zaxby's", "bojangles'", "jack in the box", "carl's jr.",
                           "hardee's", "long john silver's", "checkers", "rally's", "del taco", "church's chicken",
                           "polo tropical", "el pollo loco", "taco john's", "culver's", "raising cane's"]
    browser_apps = ["chrome", "firefox", "edge", "safari", "opera", "brave", "vivaldi", "tor", "duckduckgo"]
    if any(keyword in app_name.lower() for keyword in development_apps) or any(keyword in app_name.lower() for keyword in ide_apps):
        return "Development"
    elif any(keyword in app_name.lower() for keyword in gaming_apps):
        return "Gaming"
    elif any(keyword in app_name.lower() for keyword in meeting_apps):
        return "Meeting"
    elif any(keyword in app_name.lower() for keyword in streaming_apps):
        return "Streaming"
    elif any(keyword in app_name.lower() for keyword in design_apps):
        return "Design"
    elif any(keyword in app_name.lower() for keyword in productivity_apps):
        return "Productivity"
    elif any(keyword in app_name.lower() for keyword in finance_apps):
        return "Finance"
    elif any(keyword in app_name.lower() for keyword in health_and_fitness_apps):
        return "Health & Fitness"
    elif any(keyword in app_name.lower() for keyword in news_and_magazines_apps):
        return "News & Magazines"
    elif any(keyword in app_name.lower() for keyword in social_media_apps) or any(keyword in app_name.lower() for keyword in communication_apps):
        return "Social Media"
    elif any(keyword in app_name.lower() for keyword in travel_apps):
        return "Travel"
    elif any(keyword in app_name.lower() for keyword in food_and_drink_apps):
        return "Food & Drink"
    elif any(keyword in app_name.lower() for keyword in browser_apps):
        return "Browser"
    else:
        return "Other"


def save_summary(summary, filename):
    os.makedirs(aggregate_data_folder, exist_ok=True)
    summary_file_path = os.path.join(aggregate_data_folder, filename)
    with open(summary_file_path, 'w') as summary_file:
        json.dump(summary, summary_file, indent=4)
    print(f"Summary saved to: {summary_file_path}")


def main():
    aggregated_data_final = aggregate_and_summarize_usage_data()
    save_summary(aggregated_data_final, "usage_data.json")


if __name__ == "__main__":
    main()
