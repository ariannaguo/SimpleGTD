
window.gtd = {};
//window._ = window.gtd;

window.gtd.week_range = function (d) {
    d = new Date(d);
    d.setHours(0, 0, 0, 0);
    var day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6 : 1); // adjust when day is sunday
    return { "start": new Date(d.setDate(diff)), "end": new Date(d.setDate(diff + 7))};
};