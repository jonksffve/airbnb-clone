import { createSlice } from '@reduxjs/toolkit';

const initialState = {
	listings: [],
};

const listingsSlice = createSlice({
	name: 'listings',
	initialState,
	reducers: {
		addListings: (state, action) => {
			state.listings = action.payload.listings;
		},
		appendListing: (state, action) => {
			state.listings.push(action.payload.listing);
		},
	},
});

export const listingsActions = listingsSlice.actions;
export default listingsSlice.reducer;
