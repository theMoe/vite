export const currencyNoFractionFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0
});

export const currencyFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 2
});

export const currencySmallFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 4
});

export const formatter = new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 2
});

export const tokenFormatter = new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 6
});

export function roundToNthDecimal(number, n) {
    return Math.round(number * Math.pow(10, n)) / Math.pow(10, n);
}

export function getCurrentCycle() {
    return Math.floor((Date.now() / 1000 - 1558411200) / 24 / 3600);
}

export function downloadFileFromResponse(name, blob) {
    const href = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.setAttribute('download', name);
    document.body.appendChild(link);
    link.click();
}

export function parseDate(dateString) {
    const date = new Date(dateString);
    return new Date(date.getTime() - date.getTimezoneOffset() * 60 * 1000);
}

export function getDelayString(dateInMs) {
    if (isNaN(dateInMs)) {
        return "-"
    }
    let delay = Math.round((Date.now() - dateInMs) / 1000);
    if (delay < 60) {
        return delay + " secs ago";
    } else if (delay < 3600) {
        return Math.round(delay / 60) + " mins ago";
    } else if (delay < 86400) {
        return Math.round(delay / 3600) + " hours ago";
    } else {
        return Math.round(delay / 86400) + " days ago";
    }
}

export function cutString(string) {
    return string.substring(0, 10) + "...";
}