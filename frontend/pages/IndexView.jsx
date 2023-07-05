import { Fragment, useCallback, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getListingAPI } from '../api/AuthAPI';
import { useSelector } from 'react-redux';
import WrapperContent from '../components/UIhelpers/WrapperContent';
import IsEmpty from '../components/Listings/IsEmpty';
import ListingCard from '../components/Listings/ListingCard';
import Spinner from '../components/UIhelpers/Spinner';
import Categories from '../components/Menu/Categories';

const IndexView = () => {
	const user = useSelector((state) => state.user);
	const [listings, setListings] = useState([]);
	const [isLoading, setIsLoading] = useState(undefined);
	const [isEmpty, setIsEmpty] = useState(undefined);
	const [searchParams, setSearchParams] = useSearchParams();

	const handleReset = useCallback(() => {
		setSearchParams({});
	}, [setSearchParams]);

	useMemo(async () => {
		if (!user.token) return;
		await getListingAPI(
			user.token,
			setListings,
			setIsLoading,
			setIsEmpty,
			searchParams
		);
	}, [user.token, searchParams]);

	return (
		<Fragment>
			<div className='mb-5 w-full bg-white shadow-sm'>
				<Categories />
			</div>
			{isEmpty && (
				<IsEmpty
					onClick={handleReset}
					showReset={searchParams.size !== 0}
				/>
			)}
			<WrapperContent>
				{isLoading && <Spinner />}
				{!isLoading && (
					<div
						className='grid
							grid-cols-1
							gap-8
							sm:grid-cols-2
							md:grid-cols-3
							lg:grid-cols-4
							xl:grid-cols-5
							2xl:grid-cols-6'
					>
						{listings.map((item) => (
							<ListingCard
								key={item.id}
								data={item}
								token={user.token}
							/>
						))}
					</div>
				)}
			</WrapperContent>
		</Fragment>
	);
};

export default IndexView;
