
window.gtd = {};
//window._ = window.gtd;

gtd.dateNames = {
    dayNames: [
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ],
    shortDayNames: [
        "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
    ],
    monthNames: [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ],
    shortMonthNames: [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
};

gtd.week_range = function (d) {
    d = new Date(d);
    d.setHours(0, 0, 0, 0);
    var day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6 : 1); // adjust when day is sunday
    return { "start": new Date(d.setDate(diff)), "end": new Date(d.setDate(diff + 7) - 1)};
};

gtd.toDateString = function (dt) {
    return (dt.getMonth() + 1) + "/" + dt.getDate() + "/" + dt.getFullYear();
};

gtd.toWeekdayString = function (dt) {
    return (gtd.dateNames.shortMonthNames[dt.getMonth()]) + ". " + dt.getDate() + " (" +
            gtd.dateNames.shortDayNames[dt.getDay()] + ")";
};