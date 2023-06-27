import { createSlice } from '@reduxjs/toolkit';

const initialState = {
	showRegisterModal: false,
	showLoginModal: false,
	showRentModal: false,
};

const uiSlice = createSlice({
	name: 'ui',
	initialState,
	reducers: {
		showRegisterModal: (state) => {
			state.showRegisterModal = true;
		},
		closeRegisterModal: (state) => {
			state.showRegisterModal = false;
		},
		showLoginModal: (state) => {
			state.showLoginModal = true;
		},
		closeLoginModal: (state) => {
			state.showLoginModal = false;
		},
		showRentModal: (state) => {
			state.showRentModal = true;
		},
		closeRentModal: (state) => {
			state.showRentModal = false;
		},
	},
});

export const uiActions = uiSlice.actions;
export default uiSlice.reducer;
