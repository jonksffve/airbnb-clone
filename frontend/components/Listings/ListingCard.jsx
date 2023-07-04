import HeartButton from '../UIhelpers/Buttons/HeartButton';
import { getByValue } from '../../hooks/WorldCountries';
import { Link } from 'react-router-dom';
import { useMemo } from 'react';
import { format } from 'date-fns';
import Button from '../UIhelpers/Buttons/Button';

const ListingCard = ({
	data,
	token,
	onAction,
	actionID,
	actionLabel,
	isLoading,
	isReservation = false,
}) => {
	const fullLocation = getByValue(data?.location);

	const reservationDate = useMemo(() => {
		if (!isReservation) return undefined;

		const startDate = new Date(data.start_date);
		const endDate = new Date(data.end_date);

		return `${format(startDate, 'PP')} - ${format(endDate, 'PP')}`;
	}, [isReservation, data.end_date, data.start_date]);

	return (
		<div className='group col-span-1 cursor-pointer'>
			<div className='flex w-full flex-col gap-2'>
				<div className='relative aspect-square w-full overflow-hidden rounded-xl'>
					<Link to={`/${data.id}`}>
						<img
							className='h-full w-full object-cover transition group-hover:scale-110'
							src={data.image}
							alt=''
						/>
					</Link>
					<div className='absolute right-3 top-3'>
						<HeartButton
							token={token}
							liked={data.is_liked}
							listingID={data.id}
						/>
					</div>
				</div>
				<div className='font-semibold'>
					{fullLocation?.label}, {fullLocation?.region}
				</div>
				<div className='text-sm font-light text-neutral-500'>
					{reservationDate || data.category?.name}
				</div>
				<div className='flex flex-row items-center gap-1'>
					<div className='font-semibold'>$ {data.price}</div>
					{!reservationDate && <div className='font-light'>/ night</div>}
				</div>
				{onAction && actionLabel && (
					<Button
						disabled={isLoading}
						small
						label={actionLabel}
						onClick={() => {
							onAction(actionID);
						}}
					/>
				)}
			</div>
		</div>
	);
};

export default ListingCard;
