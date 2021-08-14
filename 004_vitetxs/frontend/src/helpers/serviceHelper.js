export function serialize(obj) {
    let str = [];
    for(const key in obj) {
        if (obj[key]) {
            if (Array.isArray(obj[key])) {
                for (const i of obj[key]) {
                    str.push(encodeURIComponent(key) + "=" + encodeURIComponent(i));   
                }
            } else {
                str.push(encodeURIComponent(key) + "=" + encodeURIComponent(obj[key]));
            }
        }
    }
    
    str = str.join("&");

    if (str !== "") {
        str = "?" + str;
    }

    return str;
}