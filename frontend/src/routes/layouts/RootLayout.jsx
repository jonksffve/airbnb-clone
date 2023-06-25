import { Fragment } from 'react';
import { Outlet } from 'react-router-dom';
import MainNavigation from '../../../components/Menu/Navbar';

const RootLayout = () => {
	return (
		<Fragment>
			<MainNavigation />
			<main>
				<Outlet />
			</main>
		</Fragment>
	);
};

export default RootLayout;
