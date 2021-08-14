import { optionsForGetRequest } from '../helpers/authHeader';

export const sbpService = {
    getSbpList
}

const url = process.env.VUE_APP_API_URL;

async function getSbpList() {
    return await fetch(`${url}/sbp/`, optionsForGetRequest);
}