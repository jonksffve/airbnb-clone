import { createBrowserRouter } from 'react-router-dom';
import RootLayout from './layouts/RootLayout';

export const router = createBrowserRouter([
	{
		path: '/',
		element: <RootLayout />,
		children: [
			{
				index: true,
				element: (
					<h2 className='bg-slate-500'>Im the element body itsel.</h2>
				),
			},
		],
	},
]);
