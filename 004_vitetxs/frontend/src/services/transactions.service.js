import { serialize } from '../helpers/serviceHelper';
import { optionsForGetRequest } from '../helpers/authHeader';

export const transactionsService = {
    getStatistics,
    getCurrentTransactionListData
}

const url = process.env.VUE_APP_API_URL;

async function getStatistics(viteAddress, params) {
    const paramsString = serialize(params);
    return await fetch(`${url}/transactions/${viteAddress}${paramsString}`, optionsForGetRequest);
}

async function getCurrentTransactionListData()  {
    return await fetch(`${url}/transactions/`, optionsForGetRequest);
}