import { useMemo } from 'react';
import { Outlet } from 'react-router-dom';
import MainNavigation from '../../../components/Menu/Navbar';
import RegisterModal from '../../../components/Modals/RegisterModal';
import LoginModal from '../../../components/Modals/LoginModal';
import { getUserInformationAPI } from '../../../api/AuthAPI';
import { useDispatch } from 'react-redux';
import { userActions } from '../../../store/user-slice';
import RentModal from '../../../components/Modals/RentModal';
import SearchModal from '../../../components/Modals/SearchModal';

const RootLayout = () => {
	const dispatch = useDispatch();

	useMemo(async () => {
		const token = localStorage.getItem('auth_token');
		if (!token) return;

		await getUserInformationAPI(token).then((response) => {
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
		});
	}, [dispatch]);

	return (
		<div className='flex h-[100vh] flex-col'>
			<MainNavigation />
			<main>
				<Outlet />
			</main>
			<SearchModal />
			<RentModal />
			<RegisterModal />
			<LoginModal />
		</div>
	);
};

export default RootLayout;
