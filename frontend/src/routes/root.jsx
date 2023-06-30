import { createBrowserRouter } from 'react-router-dom';
import RootLayout from './layouts/RootLayout';
import Index from '../../pages/Index';
import ListingDetail from '../../pages/ListingDetail';

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
		],
	},
]);
