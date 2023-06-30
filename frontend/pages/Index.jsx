import { useCallback, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { readListingAPI } from '../api/AuthAPI';
import { useDispatch, useSelector } from 'react-redux';
import Container from '../components/UIhelpers/Container';
import IsEmpty from '../components/Listings/IsEmpty';
import ListingCard from '../components/Listings/ListingCard';
import { listingsActions } from '../store/listings-slice';

const Index = () => {
	const user = useSelector((state) => state.user);
	const listings = useSelector((state) => state.listings);
	const dispatch = useDispatch();

	const [isLoading, setIsLoading] = useState(undefined);
	const [isEmpty, setIsEmpty] = useState(undefined);
	const [searchParams, setSearchParams] = useSearchParams();

	const handleReset = useCallback(() => {
		setSearchParams({});
	}, [setSearchParams]);

	useMemo(() => {
		if (!user.token) return;
		setIsLoading(true);
		readListingAPI(
			user.token,
			(value) => {
				dispatch(listingsActions.addListings(value));
			},
			setIsLoading,
			setIsEmpty
		);
	}, [user.token, dispatch]);

	if (isEmpty) {
		return (
			<IsEmpty
				onClick={handleReset}
				showReset={searchParams.size !== 0}
			/>
		);
	}

	return (
		<Container>
			<div
				className='grid
							grid-cols-1
							gap-8
							pt-24
							sm:grid-cols-2
							md:grid-cols-3
							lg:grid-cols-4
							xl:grid-cols-5
							2xl:grid-cols-6'
			>
				{listings.listings.map((item) => (
					<ListingCard
						key={item.id}
						data={item}
					/>
				))}
			</div>
		</Container>
	);
};

export default Index;