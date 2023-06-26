import { createSlice } from '@reduxjs/toolkit';

const initialState = {
	token: undefined,
	userID: undefined,
	first_name: undefined,
	last_name: undefined,
	email: undefined,
	avatar: undefined,
	loggedIn: false,
};

const userSlice = createSlice({
	name: 'user',
	initialState,
	reducers: {
		loginUser: (state, action) => {
			const { token, userID, first_name, last_name, email, avatar } =
				action.payload;
			state.userID = userID;
			state.token = token;
			state.first_name = first_name;
			state.last_name = last_name;
			state.email = email;
			state.avatar = avatar;
			state.loggedIn = true;
		},
		logoutUser: (state) => {
			state.userID = undefined;
			state.token = undefined;
			state.first_name = undefined;
			state.last_name = undefined;
			state.email = undefined;
			state.avatar = undefined;
			state.loggedIn = false;
		},
	},
});

export const userActions = userSlice.actions;
export default userSlice.reducer;
