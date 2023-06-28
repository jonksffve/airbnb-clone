import countries from 'world-countries';

const formattedCountries = countries.map((country) => {
	return {
		value: country.cca2,
		label: country.name.common,
		flag: country.flag,
		latlng: country.latlng,
		region: country.region,
	};
});

export const getAll = () => formattedCountries;

export const getByValue = (value) => {
	return formattedCountries.find((country) => country.value === value);
};
