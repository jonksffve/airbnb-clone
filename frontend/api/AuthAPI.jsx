import axios from 'axios';
import { toast } from 'react-toastify';
import { toastOptions } from '../config/toastifyConfig';
import { ENDPOINT_REGISTER, ENDPOINT_TOKEN } from '../config/apiRoutesConfig';

export const registerUserAPI = async (data, setIsLoading) => {
	try {
		const response = await axios.post(ENDPOINT_REGISTER, data, {
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
		const response = await axios.post(ENDPOINT_TOKEN, data, {
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
