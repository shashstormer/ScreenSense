var timer;
document.addEventListener("DOMContentLoaded", function () {
    fetchData();
});
var last_fetched = window.location.pathname.slice(5);
function back(e) {
    e.preventDefault();
    clearInterval(timer);
    last_fetched = last_fetched.slice(0, -1).split("/").slice(0, -1).join("/") + "/";
    fetchData(last_fetched);
    timer = setInterval(fetchData, 1000);
}
document.getElementById("back").addEventListener("click", back);
window.addEventListener('popstate', back);

async function fetchData(route=window.location.pathname.slice(5)) {
    if (route === "") {
        route = "/";
    } else if (route.slice(-1) !== "/") {
        route += "/";
    }
    window.history.pushState({}, '', ("/view/"+route).replace(/\/\//g, '/'));
    last_fetched = route;
    try {
        const response = await fetch('/api'+route);
        const data = await response.json();
        displayEndpoints(data);
    } catch (error) {
        console.log("Error fetching data:", error);
    }
}

function secondsToHMS(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    const hoursText = hours > 0 ? `${hours} ${hours === 1 ? 'hour' : 'hours'}` : '';
    const minutesText = minutes > 0 ? `${minutes} ${minutes === 1 ? 'minute' : 'minutes'}` : '';
    const secondsText = remainingSeconds > 0 ? `${remainingSeconds.toFixed(2)} ${remainingSeconds === 1 ? 'second' : 'seconds'}` : '';
    const timeArray = [hoursText, minutesText, secondsText].filter(Boolean);

    return timeArray.join(' ');
}

function formatDateRoute(input) {
    const parts = input.split('/').filter(part => part !== ''); // Remove empty parts
    function getYearString(year) {
        return year;
    }

    function getMonthString(year, month) {
        // Convert numeric month to its name
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        const monthName = monthNames[parseInt(month, 10) - 1];
        return `${monthName} ${year}`;
    }

    function getDayString(year, month, day) {
        const formattedDay = getFormattedDay(day);
        const formattedMonth = getMonthString(year, month);
        return `${formattedDay} ${formattedMonth}`;
    }

    function getCategoryString(year, month, day, category) {
        const formattedDay = getDayString(year, month, day);
        return `${formattedDay} (${category})`;
    }

    function getAppString(year, month, day, category, app) {
        const formattedCategory = getCategoryString(year, month, day, category);
        return `${formattedCategory} - ${app}`;
    }

    function getFormattedDay(day) {
        const numericDay = parseInt(day, 10);
        const suffixes = ['th', 'st', 'nd', 'rd'];
        const suffix = numericDay % 100 > 10 && numericDay % 100 < 14 ? 'th' : suffixes[(numericDay % 10 < 4) ? numericDay % 10 : 0];
        return `${numericDay}${suffix}`;
    }
    parts.unshift('');
    if (parts.length === 0) {
        return "All Time";
    } else if (parts.length === 1) {
        return "All Time";
    } else if (parts.length === 2) {
        const year = parts[1];
        return getYearString(year);
    } else if (parts.length === 3) {
        const year = parts[1];
        const month = parts[2];
        return getMonthString(year, month);
    } else if (parts.length === 4) {
        const year = parts[1];
        const month = parts[2];
        const day = parts[3];
        return getDayString(year, month, day);
    } else if (parts.length === 5) {
        const year = parts[1];
        const month = parts[2];
        const day = parts[3];
        const category = parts[4];
        return getCategoryString(year, month, day, category).replace(/%20/g, ' ');
    } else if (parts.length === 6) {
        const year = parts[1];
        const month = parts[2];
        const day = parts[3];
        const category = parts[4];
        const app = parts[5];
        return getAppString(year, month, day, category, app).replace(/%20/g, ' ');
    } else {
        return "";
    }
}


function displayEndpoints(data) {
    const appContainer = document.getElementById('app');
    const usageFor = formatDateRoute(last_fetched.slice(0, -1));
    // Generate HTML for all available API endpoints
    let endpointsHTML = `<h1>Usage Data for ${usageFor}</h1><div style="display: flex;flex-wrap: wrap;">`;
    for (const key1 in data) {
        for (const key2 in data[key1]) {
            endpointsHTML += "<div class='app'>";
            endpointsHTML += `<div onclick="fetchData('${last_fetched+key2}/')" style="font-size: 20px;text-decoration: underline"><strong>${formatDateRoute(last_fetched+key2)}</strong></div><br><br>`;
            for (const key3 in data[key1][key2]) {
                endpointsHTML += `<div><span style="font-weight: 600">${key3}</span>: ${secondsToHMS(data[key1][key2][key3])}</div><br>`;
            }
            endpointsHTML += '</div>';
        }
    }
    endpointsHTML += '</div>';
    appContainer.innerHTML = endpointsHTML;
}

timer = setInterval(fetchData, 1000);
