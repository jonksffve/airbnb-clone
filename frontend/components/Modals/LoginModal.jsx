import { useState, useCallback } from 'react';
import Modal from '../UIhelpers/Modal';
import { useDispatch, useSelector } from 'react-redux';
import { uiActions } from '../../store/ui-slice';
import { userActions } from '../../store/user-slice';
import Input from '../UIhelpers/Inputs/Input';
import Heading from './Heading';
import { useForm } from 'react-hook-form';
import Button from '../UIhelpers/Button';
import { FcGoogle } from 'react-icons/fc';
import { AiFillGithub } from 'react-icons/ai';
import { createAuthorizationAPI } from '../../api/AuthAPI';

const LoginModal = () => {
	const uiState = useSelector((state) => state.ui);
	const dispatch = useDispatch();
	const [isLoading, setIsLoading] = useState(false);

	const {
		register,
		handleSubmit,
		reset,
		formState: { errors },
	} = useForm({
		defaultValues: {
			username: '',
			password: '',
		},
	});

	const handleClose = useCallback(() => {
		dispatch(uiActions.closeLoginModal());
		reset();
	}, [dispatch, reset]);

	const onSubmit = useCallback(
		async (data) => {
			const response = await createAuthorizationAPI(data, setIsLoading);

			if (response.status === 200) {
				const { token, user } = response.data;
				handleClose();
				dispatch(
					userActions.loginUser({
						token: token,
						userID: user.id,
						first_name: user.first_name,
						last_name: user.last_name,
						email: user.email,
						avatar: user.avatar,
					})
				);
				localStorage.setItem('auth_token', token);
			}
		},
		[dispatch, handleClose]
	);

	const bodyContent = (
		<div className='flex flex-col gap-4'>
			<Heading
				title='Welcome to Airbnb'
				subtitle='Login'
			/>
			<Input
				id='username'
				label='Email'
				type='email'
				disabled={isLoading}
				register={register}
				errors={errors}
				required
			/>
			<Input
				id='password'
				type='password'
				label='Password'
				disabled={isLoading}
				register={register}
				errors={errors}
				required
			/>
		</div>
	);

	const footerContent = (
		<div className='mt-3 flex flex-col gap-4'>
			<Button
				label='Continue with Google'
				onClick={() => {}}
				outline
				icon={FcGoogle}
			/>
			<Button
				label='Continue with GitHub'
				onClick={() => {}}
				outline
				icon={AiFillGithub}
			/>
			<div
				className='mt-4 
			text-center
			font-light
			text-neutral-500'
			>
				<div className='flex flex-row items-center justify-center gap-2'>
					<div>First time in Airbnb?</div>
					<div
						onClick={() => {
							dispatch(uiActions.closeLoginModal());
							dispatch(uiActions.showRegisterModal());
						}}
						className='cursor-pointer
					text-neutral-800
					hover:underline'
					>
						Register
					</div>
				</div>
			</div>
		</div>
	);

	return (
		<Modal
			disabled={isLoading}
			isOpen={uiState.showLoginModal}
			onClose={handleClose}
			title='User authentication'
			actionLabel='Login'
			onSubmit={handleSubmit(onSubmit)}
			body={bodyContent}
			footer={footerContent}
		/>
	);
};

export default LoginModal;
