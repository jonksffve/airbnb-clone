import { Fragment, useCallback, useMemo, useState } from 'react';
import Heading from '../components/Modals/Heading';
import Container from '../components/UIhelpers/Container';
import { useSelector } from 'react-redux';
import {
	deleteReservationAPI,
	getListingReservationsAPI,
} from '../api/AuthAPI';
import ListingCard from '../components/Listings/ListingCard';
import { useNavigate } from 'react-router-dom';
import Spinner from '../components/UIhelpers/Spinner';

const Trips = () => {
	const [tripsData, setTripsData] = useState([]);
	const [isLoading, setIsLoading] = useState(undefined);
	const user = useSelector((state) => state.user);
	const navigate = useNavigate();

	useMemo(async () => {
		if (!user.token) return;
		await getListingReservationsAPI(user.token, setTripsData, setIsLoading);
	}, [user.token]);

	const handleCancel = useCallback(
		async (reservationID) => {
			await deleteReservationAPI(reservationID, user.token).then(() => {
				navigate(0);
			});
		},
		[user.token, navigate]
	);

	return (
		<Container>
			{isLoading && <Spinner />}
			{!isLoading && (
				<Fragment>
					<Heading
						title='All your trips'
						subtitle='Where you have been (and where you will be...)'
					/>
					<div
						className='mt-10
                        grid 
                        grid-cols-1 
                        gap-8 
                        sm:grid-cols-2 
                        md:grid-cols-3
                        lg:grid-cols-4
                        xl:grid-cols-5
                        2xl:grid-cols-6
                        '
					>
						{tripsData.map((trip) => (
							<ListingCard
								key={trip.id}
								data={{
									start_date: trip.start_date,
									end_date: trip.end_date,
									...trip.listing,
								}}
								token={user.token}
								isReservation
								onCancel={handleCancel}
								actionID={trip.id}
								isLoading={isLoading}
							/>
						))}
					</div>
				</Fragment>
			)}
		</Container>
	);
};

export default Trips;
