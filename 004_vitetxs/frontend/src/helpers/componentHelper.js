export function copyToClipboard(toCopy) {
  const element = document.createElement("input");
  element.value = toCopy;
  document.body.appendChild(element);
  element.select();
  document.execCommand("copy");
  document.body.removeChild(element);
}

export function getColorForRank(rank) {
  switch (rank) {
    case 1:
      return "#d4af37";
    case 2:
      return "#aaa9ad";
    case 3:
      return "#a97142";
    default:
      return "#06254b";
  }
}

export function getColorForRatio(ratio) {
  if (ratio > 90) {
    return "#1cc54e";
  } else {
    return "#c91432";
  }
}

export function getColorForStatus(status) {
  if (status) {
    return "#80e09d";
  } else {
    return "#f56a5e";
  }
}

export function getCurrentCycle() {
  return Math.floor((Date.now() / 1000 - 1558411200) / 24 / 3600);
}

export function customCurrencySort(items, index, isDescending) {
  items.sort((a, b) => {
    if (
      index == "votes" ||
      index == "transaction_in_usdt" ||
      index == "amount_normalised" ||
      index == "totalSupply"
    ) {
      const numA = a[index]
      const numB = b[index]

      if (isDescending[0]) {
        return compareNumber(
          parseCurrencyToNumber(numA),
          parseCurrencyToNumber(numB)
        );
      } else {
        return compareNumber(
          parseCurrencyToNumber(numB),
          parseCurrencyToNumber(numA)
        );
      }
    } else {
      if (!isDescending[0]) {
        return a[index] < b[index] ? -1 : 1;
      } else {
        return b[index] < a[index] ? -1 : 1;
      }
    }
  });
  return items;
}

export function parseCurrencyToNumber(currency) {
  return Number(`${currency}`.replace(/[^0-9.-]+/g, ""));
}

function compareNumber(a, b) {
  return a > b ? -1 : 1;
}

export function parseLocaleDate(date) {
  const options = {
    weekday: "short",
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
    timeZoneName: "short",
  };
  return new Date(date).toLocaleDateString(undefined, options);
}

export function isViteAddress(address) {
  const addressRegex = /vite_(\w){50}/;
  return addressRegex.test(address);
}

let start;

export function startClock() {
  start = Date.now();
}

export function logTime() {
  console.log(((Date.now() - start) / 1000) + " seconds");
}