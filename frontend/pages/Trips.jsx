import { useEffect, useState } from 'react';
import Heading from '../components/Modals/Heading';
import Container from '../components/UIhelpers/Container';
import { useSelector } from 'react-redux';
import { getListingReservationsAPI } from '../api/AuthAPI';
import ListingCard from '../components/Listings/ListingCard';

useSelector;

const Trips = () => {
	const [tripsData, setTripsData] = useState([]);
	const [isLoading, setIsLoading] = useState(false);
	const user = useSelector((state) => state.user);

	useEffect(() => {
		const fetchTrips = async () => {
			if (!user.token) return;
			await getListingReservationsAPI(user.token, setTripsData, setIsLoading);
		};

		fetchTrips();
	}, [user.token]);

	const handleCancel = (reservationID) => {
		console.log('clicked cancel', reservationID);
	};

	return (
		<Container>
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
					/>
				))}
			</div>
		</Container>
	);
};

export default Trips;
