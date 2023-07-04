import { createBrowserRouter } from 'react-router-dom';
import RootLayout from './layouts/RootLayout';
import Index from '../../pages/Index';
import ListingDetail from '../../pages/ListingDetail';
import Trips from '../../pages/Trips';
import Favorites from '../../pages/Favorites';
import Reservations from '../../pages/Reservations';
import Properties from '../../pages/Properties';

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
				element: <Reservations />,
			},
			{
				path: 'properties/',
				element: <Properties />,
			},
		],
	},
]);
