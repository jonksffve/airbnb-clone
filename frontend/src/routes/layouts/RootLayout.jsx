import { Fragment, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import MainNavigation from '../../../components/Menu/Navbar';
import RegisterModal from '../../../components/Modals/RegisterModal';
import LoginModal from '../../../components/Modals/LoginModal';
import { getUserInformationAPI } from '../../../api/AuthAPI';
import { useDispatch } from 'react-redux';
import { userActions } from '../../../store/user-slice';

const RootLayout = () => {
	const dispatch = useDispatch();

	useEffect(() => {
		const fetchUser = async () => {
			const token = localStorage.getItem('auth_token');
			if (!token) return;

			const response = await getUserInformationAPI(token);

			if (response.status === 200) {
				const { key, user } = response.data;

				dispatch(
					userActions.loginUser({
						token: key,
						first_name: user.first_name,
						last_name: user.last_name,
						email: user.email,
						avatar: user.avatar,
						userID: user.id,
					})
				);
			}
		};

		fetchUser();
	}, [dispatch]);

	return (
		<Fragment>
			<MainNavigation />
			<main>
				<Outlet />
			</main>
			<RegisterModal />
			<LoginModal />
		</Fragment>
	);
};

export default RootLayout;
