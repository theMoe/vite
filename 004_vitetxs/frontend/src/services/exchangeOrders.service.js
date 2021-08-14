import { optionsForGetRequest } from '../helpers/authHeader';
import { serialize } from '../helpers/serviceHelper';

export const exchangeOrdersService = {
    getMultiselectData,
    getStatistics
}

const url = process.env.VUE_APP_API_URL;

async function getMultiselectData() {
    return await fetch(`${url}/markets/`, optionsForGetRequest);
}

async function getStatistics(viteAddress, params) {
    const paramsString = serialize(params);
    
    return await fetch(`${url}/orders/${viteAddress}${paramsString}`, optionsForGetRequest);
}