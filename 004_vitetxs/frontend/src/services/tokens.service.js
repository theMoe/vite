import { optionsForGetRequest } from '../helpers/authHeader';

export const tokensService = {
    getTokenData
}

const url = process.env.VUE_APP_API_URL;

async function getTokenData() {
    return await fetch(`${url}/tokens/list`, optionsForGetRequest);
}