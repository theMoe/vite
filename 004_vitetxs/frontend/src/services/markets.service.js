import { optionsForGetRequest } from '../helpers/authHeader';

export const marketsService = {
    getStatistics
}

const url = process.env.VUE_APP_API_URL;

async function getStatistics(viteAddress) {
    return await fetch(`${url}/mining/order/${viteAddress}`, optionsForGetRequest);
}