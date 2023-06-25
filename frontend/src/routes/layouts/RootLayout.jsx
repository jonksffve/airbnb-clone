import { Fragment } from 'react';
import { Outlet } from 'react-router-dom';
import MainNavigation from '../../../components/Menu/Navbar';
import RegisterModal from '../../../components/Modals/RegisterModal';
import LoginModal from '../../../components/Modals/LoginModal';

const RootLayout = () => {
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
