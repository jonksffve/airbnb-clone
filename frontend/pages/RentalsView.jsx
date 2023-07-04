import { Fragment, useCallback, useMemo, useState } from 'react';
import WrapperContent from '../components/UIhelpers/WrapperContent';
import { useSelector } from 'react-redux';
import {
	deleteReservationAPI,
	getListingReservationsAPI,
} from '../api/AuthAPI';
import Heading from '../components/Modals/Heading';
import ListingCard from '../components/Listings/ListingCard';
import Spinner from '../components/UIhelpers/Spinner';
import IsEmpty from '../components/Listings/IsEmpty';
import { useNavigate } from 'react-router-dom';

const ReservationsView = () => {
	const user = useSelector((state) => state.user);
	const [reservations, setReservations] = useState([]);
	const [isLoading, setIsLoading] = useState(undefined);
	const [isEmpty, setIsEmpty] = useState(undefined);
	const navigate = useNavigate();

	useMemo(async () => {
		if (!user.token) return;
		await getListingReservationsAPI(
			user.token,
			setReservations,
			setIsLoading,
			undefined,
			true
		).then(() => {
			setIsEmpty(reservations.length === 0);
		});
	}, [user.token, reservations.length]);

	const handleCancel = useCallback(
		async (id) => {
			await deleteReservationAPI(id, user.token, true).then(() => {
				navigate(0);
			});
		},
		[user.token, navigate]
	);

	if (isEmpty) {
		return <IsEmpty />;
	}

	return (
		<WrapperContent>
			{isLoading && <Spinner />}
			{!isLoading && (
				<Fragment>
					<Heading
						title='All reservations made on your properties'
						subtitle='Check them out'
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
						{reservations.map((reservation) => (
							<ListingCard
								key={reservation.id}
								data={{
									...reservation.listing,
									start_date: reservation.start_date,
									end_date: reservation.end_date,
								}}
								token={user.token}
								onAction={handleCancel}
								actionID={reservation.id}
								actionLabel='Cancel renting'
								isLoading={isLoading}
								isReservation
							/>
						))}
					</div>
				</Fragment>
			)}
		</WrapperContent>
	);
};

export default ReservationsView;
