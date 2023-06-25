import { AiOutlineMenu } from 'react-icons/ai';
import Avatar from '../UIhelpers/Avatar';
import { useCallback, useState } from 'react';
import MenuItem from './MenuItem';
import { useDispatch } from 'react-redux';
import { uiActions } from '../../store/ui-slice';

const UserMenu = () => {
	const [isOpen, setIsOpen] = useState(false);
	const dispatch = useDispatch();

	const toggleOpen = useCallback(() => {
		setIsOpen(!isOpen);
	}, [isOpen]);

	return (
		<div className='relative'>
			<div className='flex flex-row items-center gap-3'>
				<div className='hidden cursor-pointer rounded-full px-4 py-3 text-sm font-semibold transition hover:bg-neutral-100 md:block'>
					Air your home
				</div>
				<div
					className='flex cursor-pointer flex-row items-center gap-3 rounded-full border-[1px] border-neutral-200 p-4 transition hover:shadow-md md:px-2 md:py-1'
					onClick={toggleOpen}
				>
					<AiOutlineMenu />
					<div className='hidden md:block'>
						<Avatar />
					</div>
				</div>
			</div>
			{isOpen && (
				<div className='absolute right-0 top-12 w-[40vw] overflow-hidden rounded-xl bg-white text-sm shadow-md md:w-3/4'>
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
				</div>
			)}
		</div>
	);
};

export default UserMenu;
