import axios from 'axios';
import { toast } from 'react-toastify';
import { toastOptions } from '../config/toastifyConfig';
import {
	ENDPOINT_ACCOUNT,
	ENDPOINT_AUTH,
	ENDPOINT_FAVORITE,
	ENDPOINT_LISTING,
	ENDPOINT_RESERVATION,
} from '../config/apiRoutesConfig';

//? CRUD HELPER FUNCTIONS

//* CREATE [POST] REQUESTS

/**
 * Function that tries to create a newuser in the backend.
 *
 * @async
 * @param {object} data - Data payload to be sent.
 * @param {function(boolean):void} setIsLoading - Callback that will set the component's loading state.
 * @returns Returns response object that contains user object information and extras**
 * @throws Will throw error messages if it fails.
 */
export const createNewUserAPI = async (data, setIsLoading) => {
	try {
		setIsLoading(true);
		const response = await axios.post(ENDPOINT_ACCOUNT, data);
		toast.success('User created', toastOptions);
		return response;
	} catch (error) {
		if (error.response.data) {
			for (const err in error.response.data) {
				toast.error(`${err}: ${error.response.data[err]}`, toastOptions);
			}
		}
		throw error.response;
	} finally {
		setIsLoading(false);
	}
};

/**
 * Function that tries to create token authotization in the backend.
 *
 * @async
 * @param {object} data - Data payload to be sent.
 * @param {function(boolean):void} setIsLoading - Callback that will set the component's loading state.
 * @returns Returns response object with authenticated user object information and extras**
 * @throws Will throw error messages if it fails.
 */
export const createAuthorizationAPI = async (data, setIsLoading) => {
	try {
		setIsLoading(true);
		const response = await axios.post(ENDPOINT_AUTH, data);
		toast.success('User logged in', toastOptions);
		return response;
	} catch (error) {
		toast.error('Could not login. Please check credentials.', toastOptions);
		throw error.response;
	} finally {
		setIsLoading(false);
	}
};

/**
 * Function that tries to create a Listing instance object.
 *
 * @async
 * @param {object} data - Data payload to be sent.
 * @param {function(boolean):void} setIsLoading - Callback that will set the component's loading state.
 * @param {string} token - String value that represents the authorization of a given user.
 * @throws Response: with error messages if it fails.
 */
export const createListingAPI = async (data, setIsLoading, token) => {
	try {
		setIsLoading(true);
		await axios.postForm(ENDPOINT_LISTING, data, {
			headers: {
				'content-type': 'multipart/form-data',
				Authorization: `Token ${token}`,
			},
		});
		toast.success('Listing created!', toastOptions);
	} catch (error) {
		if (error.response.data) {
			for (const err in error.response.data) {
				toast.error(`${err}: ${error.response.data[err]}`, toastOptions);
			}
		}
		throw error.response;
	} finally {
		setIsLoading(false);
	}
};

/**
 * Function that tries to create a Reservation instance object on a selected listing.
 *
 * @async
 * @param {string} listingID - ID of the selected listing we're attempting to reservate.
 * @param {object} dateRange - Object containing startdate and endingdate.
 * @param {string} token - String value that represents the authorization of a given user.
 * @param {function(boolean):void} setIsReservating - Callback that will set the component's state.
 */
export const createReservationAPI = async (
	listingID,
	dateRange,
	token,
	setIsReservating
) => {
	try {
		setIsReservating(true);
		await axios.post(
			ENDPOINT_RESERVATION,
			{
				listingID,
				start_date: dateRange.startDate,
				end_date: dateRange.endDate,
			},
			{
				headers: {
					Authorization: `Token ${token}`,
				},
			}
		);
		toast.success('Reservation is made!', toastOptions);
	} catch (error) {
		toast.error('Could not create reservation', toastOptions);
	} finally {
		setIsReservating(false);
	}
};

//* READ [GET] REQUESTS

/**
 * Function that tries to get user information based on a provided token.
 *
 * @async
 * @param {string} token - String value that represents the authorization of a given user.
 * @returns Response object that contains the authenticated user information.
 * @throws Response object that contains error messages if it fails.
 */
export const getUserInformationAPI = async (token) => {
	try {
		const response = await axios.get(`${ENDPOINT_ACCOUNT}${token}/`, {
			headers: {
				Authorization: `Token ${token}`,
			},
		});
		return response;
	} catch (error) {
		toast.error('Please check credentials.', toastOptions);
		throw error.response;
	}
};

/**
 * Function that tries to retrieve a list of listing instances.
 *
 * @async
 * @param {string} token - String value that represents the authorization of a given user.
 * @param {function(Array):void} setData - Callback that sets component's data list state.
 * @param {function(boolean):void} setIsLoading - Callback to set component's loading state.
 * @param {function(boolean):void} setIsEmpty - Callback to set component's data display state.
 * @param {URLSearchParams} [params = false] - URLSearchParams to let the backend know how to filter data is optional.
 */
export const getListingAPI = async (
	token,
	setData,
	setIsLoading,
	setIsEmpty,
	params = false
) => {
	try {
		setIsLoading(true);

		let url = ENDPOINT_LISTING;

		if (params.size !== 0) {
			url += `?${params.toString()}`;
		}

		const response = await axios.get(url, {
			headers: {
				Authorization: `Token ${token}`,
			},
		});

		setData(response.data);
		setIsEmpty(response.data.length === 0);
	} catch (error) {
		setData([]);
		setIsEmpty(true);
		toast.error('Something happened, fetching data.', toastOptions);
	} finally {
		setIsLoading(false);
	}
};

/**
 * Function that tries to retrieve information of a particular Listing instance.
 *
 * @async
 * @param {string} listingID - String value that represents the ID of a particular listing
 * @param {string} token - String value that represents the authorization of a given user.
 * @param {function(Array):void} setListing - Callback that will set component's data state.
 */
export const getListingInformationAPI = async (
	listingID,
	token,
	setListing
) => {
	try {
		const response = await axios.get(`${ENDPOINT_LISTING}${listingID}/`, {
			headers: {
				Authorization: `Token ${token}`,
			},
		});
		setListing(response.data);
	} catch (error) {
		toast.error('Something went wrong!', toastOptions);
	}
};

/**
 * Function that tries to get reservations made on a particular listing
 * OR
 * Tries to get reservations made on ALL properties of the currently logged-in user
 *
 * @async
 * @param {string} token - String value that represents the authorization of a given user.
 * @param {function(Array):void} setData - Callback that sets the component's data information on successful fetching.
 * @param {function(boolean)} setIsLoading - Callback that sets the component's loading state.
 * @param {string} [listingID = undefined] - ID of a particular listing. This is optional.
 * @param {boolean} [user_properties = undefined] - Boolean to fetch currently logged-in user properties' reservations. This is optional.
 */
export const getListingReservationsAPI = async (
	token,
	setData,
	setIsLoading,
	listingID = undefined,
	user_properties = undefined
) => {
	try {
		setIsLoading(true);

		let url = ENDPOINT_RESERVATION;

		if (listingID) {
			url += `?listingID=${listingID}`;
		}

		if (user_properties) {
			url += '?user_properties';
		}

		const response = await axios.get(url, {
			headers: {
				Authorization: `Token ${token}`,
			},
		});
		setData(response.data);
	} catch (error) {
		setData([]);
		toast.error('Could not fetch data, try again!', toastOptions);
	} finally {
		setIsLoading(false);
	}
};

/**
 * Function that tries to get Favorite instances corresponding to the logged-in user
 * (All listings that the user has favorited)
 *
 * @async
 * @param {string} token - String value that represents the authorization of a given user.
 * @param {function(Array):void} setFavorites - Callback that will set the component's information state.
 * @param {function(boolean):void} setIsLoading - Callback that sets the component's loading state.
 * @param {function(boolean):void} setIsEmpty - Callback that sets the emptiness of the backend response.
 */
export const getFavoritesAPI = async (
	token,
	setFavorites,
	setIsLoading,
	setIsEmpty
) => {
	try {
		setIsLoading(true);
		const response = await axios.get(ENDPOINT_FAVORITE, {
			headers: {
				Authorization: `Token ${token}`,
			},
		});
		setFavorites(response.data);
		setIsEmpty(response.data.length === 0);
	} catch (error) {
		setFavorites([]);
		setIsEmpty(true);
		toast.error('Could not fetch data, try again!', toastOptions);
	} finally {
		setIsLoading(false);
	}
};

//* UPDATE

//* CREATE - DELETE: functions that either perform [POST] or [DELETE] requests

/**
 * Function that creates or deletes favorite instances. Based on present "like" state.
 *
 * @async
 * @param {string} listingID - String value that represents a particular listing.
 * @param {string} token - String value that represents the authorization of a given user.
 * @param {boolean} liked - Boolean value for which we determine weather to CREATE or DELETE a favorite instance.
 * @param {function(boolean):void} setLikeState - Callback that toggles the component's like state.
 */
export const favoriteCreateDeleteAPI = async (
	listingID,
	token,
	liked,
	setLikeState
) => {
	try {
		if (liked) {
			await axios.delete(`${ENDPOINT_FAVORITE}${listingID}/`, {
				headers: {
					Authorization: `Token ${token}`,
				},
			});
		} else {
			await axios.post(
				ENDPOINT_FAVORITE,
				{
					listingID,
				},
				{
					headers: {
						Authorization: `Token ${token}`,
					},
				}
			);
		}
		setLikeState(!liked);
	} catch (error) {
		toast.error('Something happened.', toastOptions);
	}
};

//* DELETE

/**
 * Function that deletes a reservation instance.
 * Can be deleted by user that made it.
 * OR
 * Can be deleted by owner of the property.
 *
 * @async
 * @param {string} reservationID - ID String that represents the reservation.
 * @param {string} token - String value that represents the authorization of a given user.
 * @param {boolean} params - Boolean value to determine who is trying to delete the reservation. (User or Property owner)
 */
export const deleteReservationAPI = async (
	reservationID,
	token,
	params = undefined
) => {
	try {
		let url = `${ENDPOINT_RESERVATION}${reservationID}/`;

		if (params) {
			url += '?is_owner';
		}

		await axios.delete(url, {
			headers: {
				Authorization: `Token ${token}`,
			},
		});
		toast.error('Reservation deleted.', toastOptions);
	} catch (error) {
		toast.error(
			'Could not delete this reservation, call support.',
			toastOptions
		);
	}
};

/**
 * Function to delete listing instances.
 *
 * @async
 * @param {string} listingID - String value that represents the listing.
 * @param {string} token - String value that represents the authorization of a given user.
 */
export const deleteListingAPI = async (listingID, token) => {
	try {
		await axios.delete(`${ENDPOINT_LISTING}${listingID}/`, {
			headers: {
				Authorization: `Token ${token}`,
			},
		});
		toast.success('Your property has been unlisted!', toastOptions);
	} catch (error) {
		toast.error('Something very wrong happened!', toastOptions);
	}
};
