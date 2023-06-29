import axios from 'axios';
import { toast } from 'react-toastify';
import { toastOptions } from '../config/toastifyConfig';
import {
	ENDPOINT_ACCOUNT,
	ENDPOINT_AUTH,
	ENDPOINT_LISTING,
} from '../config/apiRoutesConfig';

export const registerUserAPI = async (data, setIsLoading) => {
	try {
		const response = await axios.post(ENDPOINT_ACCOUNT, data, {
			withCredentials: false,
		});
		toast.success('User created', toastOptions);
		return response;
	} catch (error) {
		toast.error('Something happened', toastOptions);
		return error.response;
	} finally {
		setIsLoading(false);
	}
};

export const getAuthorizationAPI = async (data, setIsLoading) => {
	try {
		const response = await axios.post(ENDPOINT_AUTH, data, {
			withCredentials: false,
		});
		toast.success('User logged in', toastOptions);
		return response;
	} catch (error) {
		toast.error('Please check credentials.', toastOptions);
		return error.response;
	} finally {
		setIsLoading(false);
	}
};

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
		return error.response;
	}
};

export const createListingAPI = async (data, setIsLoading, token, dispatch) => {
	try {
		const response = await axios.postForm(ENDPOINT_LISTING, data, {
			withCredentials: false,
			headers: {
				'content-type': 'multipart/form-data',
				Authorization: `Token ${token}`,
			},
		});
		toast.success('Listing created!', toastOptions);
		setIsLoading(false);
		dispatch({ listing: response.data });
		return response;
	} catch (error) {
		if (error.response.data) {
			for (const err in error.response.data) {
				toast.error(`Please check: ${err}`, toastOptions);
			}
		}
		return error.response;
	}
};

export const readListingAPI = async (
	token,
	dispatch,
	setIsLoading,
	setIsEmpty
) => {
	try {
		const response = await axios.get(ENDPOINT_LISTING, {
			withCredentials: false,
			headers: {
				'content-type': 'multipart/form-data',
				Authorization: `Token ${token}`,
			},
		});
		setIsLoading(false);
		dispatch({ listings: response.data });
		setIsEmpty(response.data.length === 0);
	} catch (error) {
		setIsLoading(false);
		dispatch({ listings: [] });
		setIsEmpty(true);
		toast.error('Something happened, fetching data.', toastOptions);
	}
};
