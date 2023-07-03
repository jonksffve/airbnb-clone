import { differenceInCalendarDays } from 'date-fns';
import CalendarComponent from '../UIhelpers/CalendarComponent';
import { useCallback, useEffect, useState } from 'react';
import Button from '../UIhelpers/Button';
import { eachDayOfInterval, add } from 'date-fns';
import { createReservationAPI } from '../../api/AuthAPI';
import { useNavigate } from 'react-router-dom';
import { ROUTE_TRIPS } from '../../config/apiRoutesConfig';

const ListingReservation = ({ reservations, price, listingID, token }) => {
	const navigate = useNavigate();
	const [dateRange, setDateRange] = useState({
		startDate: new Date(),
		endDate: new Date(),
		key: 'selection',
	});
	const [disabledRange, setDisabledRange] = useState([]);
	const [totalPrice, setTotalPrice] = useState(price);
	const [isReservating, setIsReservating] = useState(false);

	const handleReservation = useCallback(async () => {
		await createReservationAPI(
			listingID,
			dateRange,
			token,
			setIsReservating
		).then(() => {
			navigate(ROUTE_TRIPS);
		});
	}, [dateRange, listingID, token, navigate]);

	const handleSelect = useCallback((ranges) => {
		setDateRange(ranges);
	}, []);

	useEffect(() => {
		if (dateRange.startDate && dateRange.endDate) {
			const daysCount = differenceInCalendarDays(
				dateRange.endDate,
				dateRange.startDate
			);

			if (daysCount && price) {
				setTotalPrice(((daysCount + 1) * price).toFixed(2));
			} else {
				setTotalPrice(price);
			}
		}
	}, [price, dateRange.startDate, dateRange.endDate]);

	useEffect(() => {
		let dates = [];

		reservations.forEach((reservation) => {
			const range = eachDayOfInterval({
				start: new Date(reservation.start_date),
				end: new Date(reservation.end_date),
			});

			dates = [...dates, ...range];
		});

		if (dates.length === 0) return;

		setDisabledRange(dates);

		if (
			dates.some((date) => date.getTime() === new Date().setHours(0, 0, 0, 0))
		) {
			const nextAvailableDate = add(new Date(dates.at(-1)), { days: 1 });

			setDateRange({
				startDate: nextAvailableDate,
				endDate: nextAvailableDate,
				key: 'selection',
			});
		}
	}, [reservations]);

	return (
		<div
			className='overflow-hidden
			rounded-xl
			border-[1px]
			border-neutral-200
			bg-white'
		>
			<div className='flex flex-row items-center gap-1 p-4'>
				<div className='text-2xl font-semibold'>$ {price}</div>
				<div className='font-light text-neutral-600'>/ night</div>
			</div>
			<hr />
			<CalendarComponent
				disabled={isReservating}
				value={dateRange}
				reservations={reservations}
				onChange={(value) => handleSelect(value.selection)}
				disabledDates={disabledRange}
			/>
			<hr />
			<div className='p-4'>
				<Button
					disabled={isReservating}
					label='Reserve'
					onClick={handleReservation}
				/>
			</div>
			<div
				className='flex
			flex-row
			items-center
			justify-between
			p-4
			text-lg
			font-semibold'
			>
				<div>Total</div>
				<div>$ {totalPrice}</div>
			</div>
		</div>
	);
};

export default ListingReservation;
