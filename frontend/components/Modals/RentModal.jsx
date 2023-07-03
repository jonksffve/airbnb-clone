import Modal from '../UIhelpers/Modal';
import { useDispatch, useSelector } from 'react-redux';
import { uiActions } from '../../store/ui-slice';
import { useMemo, useState } from 'react';
import Heading from './Heading';
import CategoryInput from '../UIhelpers/Inputs/CategoryInput';
import { useForm } from 'react-hook-form';
import CountrySelect from '../UIhelpers/Inputs/CountrySelect';
import MapDisplay from '../MapDisplay';
import BasicDetail from '../UIhelpers/Inputs/BasicDetail';
import ImagesUploadInput from '../UIhelpers/Inputs/ImagesUploadInput';
import Input from '../UIhelpers/Inputs/Input';
import { createListingAPI } from '../../api/AuthAPI';
import Spinner from '../UIhelpers/Spinner';
import { getCategories } from '../../hooks/Categories';
import { useNavigate } from 'react-router-dom';

const STEPS = {
	CATEGORY: 0,
	LOCATION: 1,
	INFO: 2,
	IMAGES: 3,
	DESCRIPTION: 4,
	PRICE: 5,
};

const RentModal = () => {
	const userState = useSelector((state) => state.user);
	const uiState = useSelector((state) => state.ui);
	const dispatch = useDispatch();
	const navigate = useNavigate();
	const [step, setStep] = useState(STEPS.CATEGORY);
	const [isLoading, setIsLoading] = useState(false);
	const [country, setCountry] = useState(undefined);

	const categories = getCategories();

	const {
		register,
		handleSubmit,
		setValue,
		watch,
		formState: { errors },
		reset,
	} = useForm({
		defaultValues: {
			category: null,
			location: null,
			guestCount: 1,
			roomCount: 1,
			bathroomCount: 1,
			image: null,
			price: 1,
			title: null,
			description: null,
		},
	});

	const category = watch('category');
	const location = watch('location');
	const guestCount = watch('guestCount');
	const roomCount = watch('roomCount');
	const bathroomCount = watch('bathroomCount');
	const image = watch('image');

	const setCustomValue = (id, value) => {
		setValue(id, value, {
			shouldDirty: true,
			shouldTouch: true,
			shouldValidate: true,
		});
	};

	const onBack = () => {
		setStep((value) => value - 1);
	};

	const onNext = () => {
		setStep((value) => value + 1);
	};

	const onSubmit = async (data) => {
		if (step !== STEPS.PRICE) return onNext();
		const response = await createListingAPI(
			data,
			setIsLoading,
			userState.token
		);

		if (response.status === 201) {
			reset();
			dispatch(uiActions.closeRentModal());
			setStep(STEPS.CATEGORY);
			navigate(0);
		}
	};

	const handleClose = () => {
		dispatch(uiActions.closeRentModal());
	};

	const actionLabel = useMemo(() => {
		if (step === STEPS.PRICE) return 'Create';
		return 'Next';
	}, [step]);

	const secondaryActionLabel = useMemo(() => {
		if (step === STEPS.CATEGORY) return undefined;
		return 'Back';
	}, [step]);

	let bodyContent = (
		<div className='flex flex-col gap-8'>
			<Heading
				title='Which of these best describes your place?'
				subtitle='Pick a category'
			/>
			<div
				className='grid
						max-h-[50vh]
						grid-cols-1
						gap-3
						overflow-y-auto
						md:grid-cols-2'
			>
				{categories.map((item) => (
					<div
						key={item.label}
						className='col-span-1'
					>
						<CategoryInput
							onClick={(category) => {
								setCustomValue('category', category);
							}}
							selected={category === item.label}
							label={item.label}
							icon={item.icon}
						/>
					</div>
				))}
			</div>
		</div>
	);

	if (step === STEPS.LOCATION) {
		bodyContent = (
			<div className='flex flex-col gap-8'>
				<Heading
					title='Where is your place located?'
					subtitle='Help guests find you!'
				/>
				<CountrySelect
					onSelect={(location) => {
						setCustomValue('location', location);
					}}
					value={location}
					setCountry={setCountry}
				/>
				<MapDisplay center={country} />
			</div>
		);
	}

	if (step === STEPS.INFO) {
		bodyContent = (
			<div className='flex flex-col gap-8'>
				<Heading
					title='Share some basic information about your place'
					subtitle='What amenities do you have?'
				/>
				<BasicDetail
					title='Guests'
					subtitle='How many guests?'
					value={guestCount}
					onChange={(value) => {
						setCustomValue('guestCount', value);
					}}
				/>
				<BasicDetail
					title='Rooms'
					subtitle='How many rooms does it have?'
					value={roomCount}
					onChange={(value) => {
						setCustomValue('roomCount', value);
					}}
				/>
				<BasicDetail
					title='Bathroom'
					subtitle='How many bathrooms does it have?'
					value={bathroomCount}
					onChange={(value) => {
						setCustomValue('bathroomCount', value);
					}}
				/>
			</div>
		);
	}

	if (step === STEPS.IMAGES) {
		bodyContent = (
			<div className='flex flex-col gap-8'>
				<Heading
					title='Upload your place images'
					subtitle='Pick images that best describe your place'
				/>
				<ImagesUploadInput
					value={image}
					onChange={(value) => setCustomValue('image', value)}
				/>
			</div>
		);
	}

	if (step === STEPS.DESCRIPTION) {
		bodyContent = (
			<div className='flex flex-col gap-8'>
				<Heading
					title='How would you describe your place?'
					subtitle='Short and sweet is best!'
				/>
				<Input
					id='title'
					label='Title'
					disabled={isLoading}
					required
					register={register}
					errors={errors}
				/>
				<hr />
				<Input
					id='description'
					label='Description'
					disabled={isLoading}
					required
					register={register}
					errors={errors}
				/>
			</div>
		);
	}

	if (step === STEPS.PRICE) {
		bodyContent = (
			<div className='flex flex-col gap-8'>
				<Heading
					title='Now, set your price'
					subtitle='How much do you charge per night?'
				/>
				<Input
					id='price'
					label='Price'
					disabled={isLoading}
					type='number'
					formatPrice
					required
					register={register}
					errors={errors}
				/>
			</div>
		);
	}

	if (isLoading) {
		bodyContent = (
			<div className='flex cursor-not-allowed flex-col gap-8'>
				<Spinner />
			</div>
		);
	}

	return (
		<Modal
			isOpen={uiState.showRentModal}
			onClose={handleClose}
			onSubmit={handleSubmit(onSubmit)}
			title='Airbnb your home!'
			body={bodyContent}
			actionLabel={actionLabel}
			secondaryActionLabel={secondaryActionLabel}
			secondaryAction={step === STEPS.CATEGORY ? undefined : onBack}
			disabled={false}
		/>
	);
};

export default RentModal;
