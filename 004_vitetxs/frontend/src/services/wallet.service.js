import { optionsForGetRequest } from '../helpers/authHeader';

export const walletService = {
    getBasicWalletData,
    getNodesByViteAddress,
    getTransactionListData,
    getTokenData
}

const url = process.env.VUE_APP_API_URL;

async function getBasicWalletData(viteAddress) {
    return await fetch(`${url}/account/quota/${viteAddress}`, optionsForGetRequest);
}

async function getNodesByViteAddress(viteAddress, cycle) {
    return await fetch(`${url}/fullnode/status/${cycle}/${viteAddress}`, optionsForGetRequest);
}

async function getTransactionListData(viteAddress)  {
    return await fetch(`${url}/fullnode/transactions/${viteAddress}`, optionsForGetRequest);
}

async function getTokenData(viteAddress)  {
    return await fetch(`${url}/account/tokens/${viteAddress}`, optionsForGetRequest);
}