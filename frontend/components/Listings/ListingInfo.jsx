import { getByValue } from '../../hooks/WorldCountries';
import { getCategory } from '../../hooks/Categories';
import Avatar from '../UIhelpers/Avatar';
import ListingCategory from './ListingCategory';
import MapDisplay from '../MapDisplay';

const ListingInfo = ({
	creator,
	category,
	description,
	roomCount,
	guestCount,
	bathroomCount,
	locationValue,
}) => {
	const coordinates = getByValue(locationValue)?.latlng;
	const category_data = getCategory(category?.name);

	return (
		<div className='col-span-4 flex flex-col gap-8'>
			<div className='flex flex-col gap-2'>
				<div
					className='flex
                flex-row
                items-center
                gap-2
                text-xl
                font-semibold'
				>
					<div>
						Hosted by {creator?.first_name} {creator?.last_name}
					</div>
					<Avatar avatar={creator?.avatar} />
				</div>
				<div className='flex flex-row items-center gap-4 font-light text-neutral-500'>
					<div>{guestCount} guests</div>
					<div>{roomCount} rooms</div>
					<div>{bathroomCount} bathrooms</div>
				</div>
			</div>
			<hr />
			{category_data && (
				<ListingCategory
					icon={category_data.icon}
					label={category_data.label}
					description={category_data.description}
				/>
			)}
			<hr />
			<div className='text-lg font-light text-neutral-500'>{description}</div>
			<hr />
			<MapDisplay center={coordinates} />
		</div>
	);
};

export default ListingInfo;
