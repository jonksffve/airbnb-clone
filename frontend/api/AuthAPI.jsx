import axios from 'axios';
import { toast } from 'react-toastify';
import { toastOptions } from '../config/toastifyConfig';

export const registerAPI = async (data, setIsLoading) => {
	try {
		await axios.post('/api/register', data);
	} catch (error) {
		toast.error('Something happened', toastOptions);
	} finally {
		setIsLoading(false);
	}
};
