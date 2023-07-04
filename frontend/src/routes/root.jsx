import { createBrowserRouter } from 'react-router-dom';
import RootLayout from './layouts/RootLayout';
import IndexView from '../../pages/IndexView';
import ListingDetailView from '../../pages/ListingDetailView';
import TripsView from '../../pages/TripsView';
import FavoritesView from '../../pages/FavoritesView';
import RentalsView from '../../pages/RentalsView';
import PropertiesView from '../../pages/PropertiesView';

export const router = createBrowserRouter([
	{
		path: '/',
		element: <RootLayout />,
		children: [
			{
				index: true,
				element: <IndexView />,
			},
			{
				path: ':listingID',
				element: <ListingDetailView />,
			},
			{
				path: 'trips/',
				element: <TripsView />,
			},
			{
				path: 'favorites/',
				element: <FavoritesView />,
			},
			{
				path: 'reservations/',
				element: <RentalsView />,
			},
			{
				path: 'properties/',
				element: <PropertiesView />,
			},
		],
	},
]);
