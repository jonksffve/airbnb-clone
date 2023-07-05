import { AiOutlineMenu } from 'react-icons/ai';
import Avatar from '../UIhelpers/Avatar';
import { useCallback, useState } from 'react';
import MenuItem from './MenuItem';
import { useDispatch, useSelector } from 'react-redux';
import { uiActions } from '../../store/ui-slice';
import { userActions } from '../../store/user-slice';
import { useNavigate } from 'react-router-dom';
import {
	ROUTE_FAVORITES,
	ROUTE_PROPERTIES,
	ROUTE_RESERVATIONS,
	ROUTE_TRIPS,
} from '../../config/apiRoutesConfig';

const UserMenu = () => {
	const user = useSelector((state) => state.user);
	const [isOpen, setIsOpen] = useState(false);
	const dispatch = useDispatch();
	const navigate = useNavigate();

	const toggleOpen = useCallback(() => {
		setIsOpen(!isOpen);
	}, [isOpen]);

	const onRent = useCallback(() => {
		if (!user.loggedIn) return dispatch(uiActions.showLoginModal());

		dispatch(uiActions.showRentModal());
	}, [dispatch, user.loggedIn]);

	return (
		<div className='relative'>
			<div className='flex flex-row items-center gap-3'>
				<div
					onClick={onRent}
					className='hidden cursor-pointer rounded-full px-4 py-3 text-sm font-semibold transition hover:bg-neutral-100 md:block'
				>
					Air your home
				</div>
				<div
					className='flex cursor-pointer flex-row items-center gap-3 rounded-full border-[1px] border-neutral-200 p-4 transition hover:shadow-md md:px-2 md:py-1'
					onClick={toggleOpen}
				>
					<AiOutlineMenu />
					<div className='hidden md:block'>
						<Avatar avatar={user.avatar} />
					</div>
				</div>
			</div>
			{isOpen && (
				<div className='absolute right-0 top-12 z-50 w-[40vw] overflow-hidden rounded-xl bg-white text-sm shadow-md md:w-3/4'>
					{user.loggedIn && (
						<div className='flex cursor-pointer flex-col'>
							<MenuItem
								onClick={() => {
									navigate(ROUTE_TRIPS);
									toggleOpen();
								}}
								label='My trips'
							/>
							<MenuItem
								onClick={() => {
									navigate(ROUTE_FAVORITES);
									toggleOpen();
								}}
								label='My favorites'
							/>
							<MenuItem
								onClick={() => {
									navigate(ROUTE_RESERVATIONS);
									toggleOpen();
								}}
								label='My rentals'
							/>
							<MenuItem
								onClick={() => {
									navigate(ROUTE_PROPERTIES);
									toggleOpen();
								}}
								label='My properties'
							/>
							<MenuItem
								onClick={() => {
									toggleOpen();
									onRent();
								}}
								label='Air my home'
							/>
							<hr />
							<MenuItem
								onClick={() => {
									localStorage.removeItem('auth_token');
									dispatch(userActions.logoutUser());
									toggleOpen();
									navigate(0);
								}}
								label='Log out'
							/>
						</div>
					)}

					{!user.loggedIn && (
						<div className='flex cursor-pointer flex-col'>
							<MenuItem
								onClick={() => {
									dispatch(uiActions.showLoginModal());
									toggleOpen();
								}}
								label='Login'
							/>
							<MenuItem
								onClick={() => {
									dispatch(uiActions.showRegisterModal());
									toggleOpen();
								}}
								label='Sign up'
							/>
						</div>
					)}
				</div>
			)}
		</div>
	);
};

export default UserMenu;
