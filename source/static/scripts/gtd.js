
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

gtd.status = {
    not_started: { id: 1, show: true },
    in_progress: { id: 2, show: true },
    completed: { id: 3, show: true },
    suspended: { id: 4, show: false },
    canceled: { id: 5, show: false }
};

gtd.status.all = [gtd.status.not_started, gtd.status.in_progress, gtd.status.completed,
                  gtd.status.suspended, gtd.status.canceled];

gtd.status.find = function (id) {
    for(var i = 0; i < this.all.length; i++){
        if (this.all[i].id == id) {
            return this.all[i];
        }
    }

    return null;
};