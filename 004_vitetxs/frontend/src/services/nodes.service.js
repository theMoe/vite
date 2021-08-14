import { optionsForGetRequest } from "../helpers/authHeader";

export const nodesService = {
  getBasicNodeData,
  getNodeListData,
  getNodeMapData
};

const url = process.env.VUE_APP_API_URL;

async function getBasicNodeData(cycles) {
  return await fetch(
    `${url}/fullnode/status/basic/${cycles}`,
    optionsForGetRequest
  );
}

async function getNodeListData(cycle) {
  return await fetch(`${url}/fullnode/cycle/${cycle}`, optionsForGetRequest);
}

async function getNodeMapData() {
  return await fetch(`${url}/fullnode/geolocations`, optionsForGetRequest);
}
