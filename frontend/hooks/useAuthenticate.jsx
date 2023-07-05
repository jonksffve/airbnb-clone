import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { uiActions } from '../store/ui-slice';
import { useNavigate } from 'react-router-dom';
import { ROUTE_HOME } from '../config/apiRoutesConfig';

export const useAuthenticate = () => {
	const user = useSelector((state) => state.user);
	const dispatch = useDispatch();
	const navigate = useNavigate();

	useEffect(() => {
		const token = localStorage.getItem('auth_token');
		if (token) return;
		navigate(ROUTE_HOME);
		dispatch(uiActions.showLoginModal());
	}, [dispatch, user.token, navigate]);
};
