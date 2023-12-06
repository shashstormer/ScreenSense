from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from config import aggregate_data_folder
import json
from aggregate import main as aggregate_data
import datetime

last_aggregated = False
app = FastAPI()


def usage_data():
    global last_aggregated
    if not last_aggregated or datetime.datetime.now() - last_aggregated > datetime.timedelta(seconds=0.3):
        last_aggregated = datetime.datetime.now()
        aggregate_data()
    return json.load(open(f"{aggregate_data_folder}/usage_data.json", "r"))


@app.get("/api")
async def get_all_years():
    return {"years": {year: usage_data()[year]["time_categories"] for year in list(usage_data().keys())}}


@app.get("/api/{year}")
async def get_year_summary(year: int):
    year = str(year)
    if str(year) not in usage_data():
        raise HTTPException(status_code=404, detail="Year not found")
    return {"months": {month: usage_data()[year]["month"][month]["time_categories"] for month in
                       list(usage_data()[year]["month"].keys())}}


@app.get("/api/{year}/{month}")
async def get_month_summary(year: int, month: int):
    year_str = str(year)
    month_str = str(month)
    if year_str not in usage_data() or month_str not in usage_data()[year_str]["month"]:
        raise HTTPException(status_code=404, detail="Month not found")
    return {"days": {day: usage_data()[year_str]["month"][month_str]["day"][day]["time_categories"] for day in
                     list(usage_data()[year_str]["month"][month_str]["day"].keys())}}


@app.get("/api/{year}/{month}/{day}")
async def get_category_summary(year: int, month: int, day: int):
    year_str = str(year)
    month_str = str(month)
    day_str = str(day)
    if year_str not in usage_data() or month_str not in usage_data()[year_str]["month"] or \
            day_str not in usage_data()[year_str]["month"][month_str]["day"]:
        raise HTTPException(status_code=404, detail="Day not found")
    return {
        day_str: {i: {"total time": usage_data()[year_str]["month"][month_str]["day"][day_str]["time_categories"][i]}
                  for i in usage_data()[year_str]["month"][month_str]["day"][day_str]["time_categories"]}}


@app.get("/api/{year}/{month}/{day}/{category}")
async def get_app_summary(year: int, month: int, day: int, category: str):
    year_str = str(year)
    month_str = str(month)
    day_str = str(day)
    if year_str not in usage_data() or month_str not in usage_data()[year_str]["month"] or \
            day_str not in usage_data()[year_str]["month"][month_str]["day"] or \
            category not in usage_data()[year_str]["month"][month_str]["day"][day_str]["usage"]:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"total_time": usage_data()[year_str]["month"][month_str]["day"][day_str]["time_categories"][category],
            "details": {
                a: {"total time": usage_data()[year_str]["month"][month_str]["day"][day_str]["usage"][category][a][
                    "total_time"]} for a
                in list(usage_data()[year_str]["month"][month_str]["day"][day_str]["usage"][category].keys())}}


@app.get("/api/{year}/{month}/{day}/{category}/{a}")
async def get_app_summary(year: int, month: int, day: int, category: str, a: str):
    year_str = str(year)
    month_str = str(month)
    day_str = str(day)
    if year_str not in usage_data() or month_str not in usage_data()[year_str]["month"] or \
            day_str not in usage_data()[year_str]["month"][month_str]["day"] or \
            category not in usage_data()[year_str]["month"][month_str]["day"][day_str]["usage"] or \
            a not in usage_data()[year_str]["month"][month_str]["day"][day_str]["usage"][category]:
        raise HTTPException(status_code=404, detail="Category not found")
    return {a: {"details": usage_data()[year_str]["month"][month_str]["day"][day_str]["usage"][category][a]["details"]}}


@app.get("/view/{data:path}")
async def get_index(data: str = None):
    return Response(open(f"./ui/web/html/index.html", "r").read())


@app.get("/")
async def get_index():
    return RedirectResponse(url="/view/")


@app.get("/js/{file}")
async def get_js(file: str):
    return Response(open(f"./ui/web/js/{file}", "r").read())


@app.get("/style/{file}")
async def get_css(file: str):
    return Response(open(f"./ui/web/style/{file}", "r").read())


@app.get("/img/{file}")
async def get_img(file: str):
    return Response(open(f"./ui/web/img/{file}", "r").read())


@app.get("/favicon.ico")
async def get_favicon():
    return Response(open(f"./ui/web/favicon.ico", "r").read())


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()
