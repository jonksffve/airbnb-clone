import { createBrowserRouter } from 'react-router-dom';
import RootLayout from './layouts/RootLayout';
import Index from '../../pages/Index';
import ListingDetail from '../../pages/ListingDetail';
import Trips from '../../pages/Trips';
import Favorites from '../../pages/Favorites';

export const router = createBrowserRouter([
	{
		path: '/',
		element: <RootLayout />,
		children: [
			{
				index: true,
				element: <Index />,
			},
			{
				path: ':listingID',
				element: <ListingDetail />,
			},
			{
				path: 'trips/',
				element: <Trips />,
			},
			{
				path: 'favorites/',
				element: <Favorites />,
			},
			{
				path: 'reservations/',
				element: <h2>My reservations</h2>,
			},
			{
				path: 'properties/',
				element: <h2>My properties</h2>,
			},
		],
	},
]);
