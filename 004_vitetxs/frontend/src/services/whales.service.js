import { optionsForGetRequest } from '../helpers/authHeader';

export const whalesService = {
    getCurrentWhaleData,
    getTopWhaleData,
    getBasicWhaleData,
    getAddressWhaleData,
    getWeekdayWhaleData,
    getWhalesPerWeekData
}

const url = process.env.VUE_APP_API_URL;

async function getCurrentWhaleData() {
    return await fetch(`${url}/whales/`, optionsForGetRequest);
}

async function getTopWhaleData() {
    return await fetch(`${url}/whales/top`, optionsForGetRequest);
}

async function getBasicWhaleData(days) {
    return await fetch(`${url}/whales/change?days=${days}`, optionsForGetRequest);
}

async function getWeekdayWhaleData() {
    return await fetch(`${url}/whales/sumbyday`, optionsForGetRequest);
}

async function getWhalesPerWeekData() {
    return await fetch(`${url}/whales/byWeek`, optionsForGetRequest);
}

async function getAddressWhaleData() {
    return await fetch(`${url}/whales/topaddress`, optionsForGetRequest);
}
