import { createBrowserRouter } from 'react-router-dom';
import RootLayout from './layouts/RootLayout';
import Index from '../../pages/Index';

export const router = createBrowserRouter([
	{
		path: '/',
		element: <RootLayout />,
		children: [
			{
				index: true,
				element: <Index />,
			},
		],
	},
]);
