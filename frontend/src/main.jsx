import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { router } from './routes/root';
import { RouterProvider } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from '../store/index';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

ReactDOM.createRoot(document.getElementById('root')).render(
	<React.StrictMode>
		<Provider store={store}>
			<RouterProvider router={router} />
		</Provider>
		<ToastContainer />
	</React.StrictMode>
);
