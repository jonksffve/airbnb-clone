import CalendarComponent from '../UIhelpers/CalendarComponent';

const ListingReservation = ({
	price,
	totalPrice,
	onChangeDate,
	dateRange,
	onSubmit,
	disabled,
	disabledDates,
}) => {
	return (
		<div
			className='overflow-hidden
			rounded-xl
			border-[1px]
			border-neutral-200
			bg-white'
		>
			<div className='flex flex-row items-center gap-1 p-4'>
				<div className='text-2xl font-semibold'>$ 1000</div>
				<div className='font-light text-neutral-600'>/ night</div>
			</div>
			<hr />
			<CalendarComponent />
			<hr />
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
				<div>$ 1000</div>
			</div>
		</div>
	);
};

export default ListingReservation;
