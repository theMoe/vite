export function authHeader() {
  let token = process.env.VUE_APP_TOKEN;

  if (token) {
    return {
      'x-access-token': token,
    };
  } else {
    return {};
  }
}

export const optionsForGetRequest = {
  method: 'GET',
  headers: authHeader()
}
