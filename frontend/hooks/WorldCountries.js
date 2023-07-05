import countries from 'world-countries';

/**
 * Array of country objects formatted in a particular way.
 */
const formattedCountries = countries.map((country) => {
	return {
		value: country.cca2,
		label: country.name.common,
		flag: country.flag,
		latlng: country.latlng,
		region: country.region,
	};
});

/**
 * Function that returns all formatted countries.
 *
 * @returns {Array} Returns array of country objects
 */
export const getAll = () => formattedCountries;

/**
 * Function that retrieves country information based on a given CCA2 ISO code.
 *
 * @param {string} value - String formatted ISO cca2 code for a particular country.
 * @returns {Object} Returns country object with its information.
 */
export const getByValue = (value) => {
	return formattedCountries.find((country) => country.value === value);
};
