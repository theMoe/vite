import { optionsForGetRequest } from '../helpers/authHeader';

export const referringService = {
    getStatistics
}

const url = process.env.VUE_APP_API_URL;

async function getStatistics(viteAddress) {
    return await fetch(`${url}/mining/invite/${viteAddress}`, optionsForGetRequest);
}