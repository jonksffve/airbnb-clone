import { useDispatch, useSelector } from 'react-redux';
import Modal from './Modal';
import { useCallback, useMemo, useState } from 'react';
import { uiActions } from '../../store/ui-slice';
import Heading from './Heading';
import CountrySelect from '../UIhelpers/Inputs/CountrySelect';
import MapDisplay from '../MapDisplay';
import CalendarComponent from '../UIhelpers/CalendarComponent';
import BasicDetail from '../UIhelpers/Inputs/BasicDetail';
import {
	createSearchParams,
	useNavigate,
	useSearchParams,
} from 'react-router-dom';
import { formatISO } from 'date-fns';
import { ROUTE_HOME } from '../../config/apiRoutesConfig';

const STEPS = {
	LOCATION: 0,
	DATE: 1,
	INFO: 2,
};

const SearchModal = () => {
	const navigate = useNavigate();
	const uiState = useSelector((state) => state.ui);
	const dispatch = useDispatch();
	const [step, setStep] = useState(STEPS.LOCATION);
	const [country, setCountry] = useState(undefined);
	const [location, setLocation] = useState(undefined);
	const [dateRange, setDateRange] = useState({
		startDate: new Date(),
		endDate: new Date(),
		key: 'selection',
	});
	const [guestCount, setGuestCount] = useState(1);
	const [roomCount, setRoomCount] = useState(1);
	const [bathroomCount, setBathroomCount] = useState(1);
	const [searchParams, setSearchParams] = useSearchParams();

	const reset = useCallback(() => {
		setStep(STEPS.LOCATION);
		setCountry(undefined);
		setLocation(undefined);
		setDateRange({
			startDate: new Date(),
			endDate: new Date(),
			key: 'selection',
		});
		setGuestCount(1);
		setRoomCount(1);
		setBathroomCount(1);
		dispatch(uiActions.closeSearchModal());
	}, [dispatch]);

	const handleClose = useCallback(() => {
		dispatch(uiActions.closeSearchModal());
	}, [dispatch]);

	const onBack = useCallback(() => {
		setStep((value) => value - 1);
	}, []);

	const onNext = useCallback(() => {
		setStep((value) => value + 1);
	}, []);

	const onSubmit = useCallback(() => {
		if (step !== STEPS.INFO) return onNext();

		const category = searchParams.get('category');

		const newQuery = {
			...(category && { category }),
			location,
			startDate: formatISO(dateRange?.startDate),
			endDate: formatISO(dateRange?.endDate),
			guestCount,
			roomCount,
			bathroomCount,
		};

		reset();
		navigate({
			pathname: ROUTE_HOME,
			search: `?${createSearchParams(newQuery)}`,
		});
	}, [
		onNext,
		step,
		bathroomCount,
		dateRange,
		location,
		guestCount,
		roomCount,
		searchParams,
		navigate,
		reset,
	]);

	const actionLabel = useMemo(() => {
		if (step === STEPS.INFO) return 'Search';
		return 'Next';
	}, [step]);

	const secondaryActionLabel = useMemo(() => {
		if (step === STEPS.LOCATION) return undefined;
		return 'Back';
	}, [step]);

	let bodyContent = (
		<div className='flex flex-col gap-8'>
			<Heading
				title='Where do you want to go?'
				subtitle='Find a location.'
			/>
			<CountrySelect
				setCountry={setCountry}
				value={location}
				onSelect={(value) => {
					setLocation(value);
				}}
			/>
			<MapDisplay center={country} />
		</div>
	);

	if (step === STEPS.DATE) {
		bodyContent = (
			<div className='flex flex-col gap-8'>
				<Heading
					title='What date suits you better?'
					subtitle='Pick some dates, make sure everyone is free!'
				/>
				<CalendarComponent
					value={dateRange}
					onChange={(value) => setDateRange(value.selection)}
				/>
			</div>
		);
	}

	if (step === STEPS.INFO) {
		bodyContent = (
			<div className='flex flex-col gap-8'>
				<Heading
					title='More information.'
					subtitle='Now, lets find the perfect place.'
				/>
				<BasicDetail
					title='Guests'
					subtitle='How many guests are you inviting?'
					value={guestCount}
					onChange={(value) => {
						setGuestCount(value);
					}}
				/>
				<BasicDetail
					title='Rooms'
					subtitle='How many rooms should it have?'
					value={roomCount}
					onChange={(value) => {
						setRoomCount(value);
					}}
				/>
				<BasicDetail
					title='Bathroom'
					subtitle='How many bathrooms?'
					value={bathroomCount}
					onChange={(value) => {
						setBathroomCount(value);
					}}
				/>
			</div>
		);
	}

	return (
		<Modal
			isOpen={uiState.showSearchModal}
			onClose={handleClose}
			onSubmit={onSubmit}
			title='Plan your next vacations!'
			body={bodyContent}
			actionLabel={actionLabel}
			secondaryAction={onBack}
			secondaryActionLabel={secondaryActionLabel}
		/>
	);
};

export default SearchModal;
