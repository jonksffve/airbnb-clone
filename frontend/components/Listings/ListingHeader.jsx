import { Fragment } from 'react';
import { getByValue } from '../../hooks/WorldCountries';
import Heading from '../Modals/Heading';
import HeartButton from '../UIhelpers/HeartButton';

const ListingHeader = ({ title, image, locationValue, id, liked, token }) => {
	const location = getByValue(locationValue);

	return (
		<Fragment>
			<Heading
				title={title}
				subtitle={`${location?.region}, ${location?.label}`}
			/>
			<div className='relative h-[60vh] w-full overflow-hidden rounded-xl'>
				<div className='flex w-full justify-center'>
					<img
						className='object-contain'
						src={image}
						alt=''
					/>
				</div>
				<div className='absolute right-5 top-5'>
					<HeartButton
						token={token}
						liked={liked}
						listingID={id}
					/>
				</div>
			</div>
		</Fragment>
	);
};

export default ListingHeader;
