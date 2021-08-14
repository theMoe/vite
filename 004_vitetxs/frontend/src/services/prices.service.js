import { optionsForGetRequest } from '../helpers/authHeader';
import { serialize } from '../helpers/serviceHelper';

export const pricesService = {
    getStatistics
}

const url = process.env.VUE_APP_API_URL;

async function getStatistics(params) {
    const paramsString = serialize(params);
    
    return await fetch(`${url}/prices/${paramsString}`, optionsForGetRequest);
}