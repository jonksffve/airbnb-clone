import HeartButton from '../UIhelpers/HeartButton';
import { getByValue } from '../../hooks/WorldCountries';
import { Link } from 'react-router-dom';

const ListingCard = ({ data, token }) => {
	const reservationDate = undefined;
	const fullLocation = getByValue(data.location);

	return (
		<div className='group col-span-1 cursor-pointer'>
			<div className='flex w-full flex-col gap-2'>
				<div className='relative aspect-square w-full overflow-hidden rounded-xl'>
					<Link to={`${data.id}`}>
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
					{reservationDate || data.category.name}
				</div>
				<div className='flex flex-row items-center gap-1'>
					<div className='font-semibold'>$ {data.price}</div>
					{!reservationDate && <div className='font-light'>/ night</div>}
				</div>
			</div>
		</div>
	);
};

export default ListingCard;
