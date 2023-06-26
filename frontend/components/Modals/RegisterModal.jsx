import { useState, useCallback } from 'react';
import Modal from '../UIhelpers/Modal';
import { useDispatch, useSelector } from 'react-redux';
import { uiActions } from '../../store/ui-slice';
import { useForm } from 'react-hook-form';
import Heading from './Heading';
import Input from '../UIhelpers/Inputs/Input';
import Button from '../UIhelpers/Button';
import { FcGoogle } from 'react-icons/fc';
import { AiFillGithub } from 'react-icons/ai';
import { registerAPI } from '../../api/AuthAPI';

const RegisterModal = () => {
	const uiState = useSelector((state) => state.ui);
	const dispatch = useDispatch();
	const [isLoading, setIsLoading] = useState(false);

	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm({
		defaultValues: {
			name: '',
			email: '',
			password: '',
		},
	});

	const onSubmit = async (data) => {
		setIsLoading(true);
		await registerAPI(data, setIsLoading);
	};

	const handleClose = useCallback(() => {
		dispatch(uiActions.closeRegisterModal());
	}, [dispatch]);

	const bodyContent = (
		<div className='flex flex-col gap-4'>
			<Heading
				title='Welcome to Airbnb'
				subtitle='Create an account'
			/>
			<Input
				id='email'
				label='Email'
				disabled={isLoading}
				register={register}
				errors={errors}
				required
			/>
			<Input
				id='name'
				label='Name'
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
					<div>Already have an account?</div>
					<div
						onClick={() => {}}
						className='cursor-pointer
					text-neutral-800
					hover:underline'
					>
						Log in
					</div>
				</div>
			</div>
		</div>
	);

	return (
		<Modal
			disabled={isLoading}
			isOpen={uiState.showRegisterModal}
			onClose={handleClose}
			title='User registration'
			actionLabel='Continue'
			onSubmit={handleSubmit(onSubmit)}
			body={bodyContent}
			footer={footerContent}
		/>
	);
};

export default RegisterModal;