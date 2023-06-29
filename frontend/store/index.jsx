import { configureStore } from '@reduxjs/toolkit';
import uiSlice from './ui-slice';
import userSlice from './user-slice';
import listingsSlice from './listings-slice';

export const store = configureStore({
	reducer: {
		ui: uiSlice,
		user: userSlice,
		listings: listingsSlice,
	},
});
