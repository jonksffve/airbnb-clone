import { useCallback, useMemo, useState } from 'react';
import { BiSearch } from 'react-icons/bi';
import { useDispatch, useSelector } from 'react-redux';
import { uiActions } from '../../store/ui-slice';
import { useSearchParams } from 'react-router-dom';
import { getByValue } from '../../hooks/WorldCountries';
import { differenceInDays } from 'date-fns';

const Search = () => {
	const user = useSelector((state) => state.user);
	const dispatch = useDispatch();
	const handleSearch = useCallback(() => {
		dispatch(uiActions.showSearchModal());
	}, [dispatch]);

	const [searchParams, setSearchParams] = useSearchParams();
	const [where, setWhere] = useState('Anywhere');
	const [guestCount, setGuestCount] = useState('Add guests');
	const [dayCount, setDayCount] = useState('Any time');

	useMemo(() => {
		if (searchParams.get('location')) {
			const location = getByValue(searchParams.get('location'));
			setWhere(location.label);
		} else {
			setWhere('Anywhere');
		}

		if (searchParams.get('guestCount')) {
			let value = '';
			value =
				searchParams.get('guestCount') === '1'
					? '1 guest'
					: `${searchParams.get('guestCount')} guests`;
			setGuestCount(value);
		} else {
			setGuestCount('Add guests');
		}

		if (searchParams.get('startDate') && searchParams.get('endDate')) {
			const days = differenceInDays(
				new Date(searchParams.get('endDate')),
				new Date(searchParams.get('startDate'))
			);

			let value = '';

			value = days === 1 ? '1 day' : `${days} days`;

			setDayCount(value);
		} else {
			setDayCount('Any time');
		}
	}, [searchParams]);

	return (
		<div
			className={`w-full 
			${user.token ? 'cursor-pointer' : 'cursor-not-allowed'}
			rounded-full 
			border-[1px] 
			py-2 
			shadow-sm 
			transition 
			hover:shadow-md 
			md:w-auto`}
			onClick={user.token && handleSearch}
		>
			<div className='flex flex-row items-center justify-between'>
				<div className='px-6 text-sm font-semibold'>{where}</div>
				<div className='hidden flex-1 border-x-[1px] px-6 text-center text-sm font-semibold sm:block'>
					{dayCount}
				</div>
				<div className='flex flex-row items-center gap-3 pl-6 pr-2 text-sm text-gray-600'>
					<div className='hidden sm:block'>{guestCount}</div>
					<div className='rounded-full bg-rose-500 p-2 text-white'>
						<BiSearch size={18} />
					</div>
				</div>
			</div>
		</div>
	);
};

export default Search;
