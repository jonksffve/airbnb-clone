import Modal from '../UIhelpers/Modal';
import { useDispatch, useSelector } from 'react-redux';
import { uiActions } from '../../store/ui-slice';
import { useMemo, useState } from 'react';
import Heading from './Heading';
import { categories } from '../Menu/Categories';
import CategoryInput from '../UIhelpers/Inputs/CategoryInput';
import { useForm } from 'react-hook-form';
import CountrySelect from '../UIhelpers/Inputs/CountrySelect';
import MapDisplay from '../MapDisplay';

const STEPS = {
	CATEGORY: 0,
	LOCATION: 1,
	INFO: 2,
	IMAGES: 3,
	DESCRIPTION: 4,
	PRICE: 5,
};

const RentModal = () => {
	const uiState = useSelector((state) => state.ui);
	const dispatch = useDispatch();
	const [step, setStep] = useState(STEPS.CATEGORY);

	const {
		register,
		handleSubmit,
		setValue,
		watch,
		formState: { errors },
		reset,
	} = useForm({
		defaultValues: {
			category: '',
			location: null,
			guestCount: 1,
			roomCount: 1,
			bathroomCount: 1,
			imageSrc: '',
			price: 1,
			title: '',
			description: '',
		},
	});

	const category = watch('category');
	const location = watch('location');

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
				/>
				<MapDisplay center={location?.latlng} />
			</div>
		);
	}

	const footerContent = '';

	return (
		<Modal
			isOpen={uiState.showRentModal}
			onClose={handleClose}
			onSubmit={onNext}
			title='Airbnb your home!'
			body={bodyContent}
			footer={footerContent}
			actionLabel={actionLabel}
			secondaryActionLabel={secondaryActionLabel}
			secondaryAction={step === STEPS.CATEGORY ? undefined : onBack}
			disabled={false}
		/>
	);
};

export default RentModal;
