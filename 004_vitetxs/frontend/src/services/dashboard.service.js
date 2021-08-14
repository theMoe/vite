import { optionsForGetRequest } from '../helpers/authHeader';

export const dashboardService = {
    getRewardGraphData,
    getDashboardCounts,
    getLastTransactions
}

const url = process.env.VUE_APP_API_URL;

async function getRewardGraphData() {
    return await fetch(`${url}/fullnode/rewards?limit=50`, optionsForGetRequest);
}

async function getDashboardCounts() {
    return await fetch(`${url}/stats/`, optionsForGetRequest);
}

async function getLastTransactions(count) {
    return await fetch(`${url}/transactions/?limit=${count}`, optionsForGetRequest);
}