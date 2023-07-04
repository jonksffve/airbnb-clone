import { useParams } from 'react-router-dom';
import ListingHeader from '../components/Listings/ListingHeader';
import { useMemo, useState } from 'react';
import { useSelector } from 'react-redux';
import {
	getListingInformationAPI,
	getListingReservationsAPI,
} from '../api/AuthAPI';
import Container from '../components/UIhelpers/Container';
import ListingInfo from '../components/Listings/ListingInfo';
import ListingReservation from '../components/Listings/ListingReservations';
import Spinner from '../components/UIhelpers/Spinner';

const ListingDetail = () => {
	const { listingID } = useParams();
	const user = useSelector((state) => state.user);
	const [listing, setListing] = useState({});
	const [isLoading, setIsLoading] = useState(undefined);
	const [reservations, setReservations] = useState([]);

	useMemo(async () => {
		if (!user.token) return;
		await getListingInformationAPI(listingID, user.token, setListing);
		await getListingReservationsAPI(
			user.token,
			setReservations,
			setIsLoading,
			listingID
		);
	}, [listingID, user.token]);

	return (
		<Container>
			{isLoading && <Spinner />}
			{!isLoading && (
				<div className='mx-auto max-w-screen-lg'>
					<div className='flex flex-col gap-6'>
						<ListingHeader
							token={user.token}
							title={listing.title}
							image={listing.image}
							locationValue={listing.location}
							id={listing.id}
							liked={listing.is_liked}
						/>
						<div
							className='mt-6
				grid
				grid-cols-1
				md:grid-cols-7
				md:gap-10'
						>
							<ListingInfo
								creator={listing.creator}
								category={listing.category}
								description={listing.description}
								roomCount={listing.roomCount}
								guestCount={listing.guestCount}
								bathroomCount={listing.bathroomCount}
								locationValue={listing.location}
							/>
							<div
								className='order-first
					mb-10
					md:order-last
					md:col-span-3'
							>
								<ListingReservation
									token={user.token}
									listingID={listing.id}
									price={listing.price}
									reservations={reservations}
								/>
							</div>
						</div>
					</div>
				</div>
			)}
		</Container>
	);
};

export default ListingDetail;
