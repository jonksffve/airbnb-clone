import { useSelector } from 'react-redux';
import Container from '../components/UIhelpers/Container';
import { Fragment, useCallback, useMemo, useState } from 'react';
import Spinner from '../components/UIhelpers/Spinner';
import Heading from '../components/Modals/Heading';
import ListingCard from '../components/Listings/ListingCard';
import { deleteListingAPI, getListingAPI } from '../api/AuthAPI';
import IsEmpty from '../components/Listings/IsEmpty';
import { useNavigate } from 'react-router-dom';

const Properties = () => {
	const user = useSelector((state) => state.user);
	const [properties, setProperties] = useState([]);
	const [isLoading, setIsLoading] = useState(undefined);
	const [isEmpty, setIsEmpty] = useState(undefined);
	const navigate = useNavigate();

	useMemo(async () => {
		if (!user.token) return;
		await getListingAPI(
			user.token,
			setProperties,
			setIsLoading,
			setIsEmpty,
			true
		);
	}, [user.token]);

	const handleDelete = useCallback(
		async (id) => {
			await deleteListingAPI(id, user.token).then(() => {
				navigate(0);
			});
		},
		[user.token, navigate]
	);

	if (isEmpty) {
		return <IsEmpty />;
	}

	return (
		<Container>
			{isLoading && <Spinner />}
			{!isLoading && (
				<Fragment>
					<Heading
						title='All your properties'
						subtitle='These are all your listed properties'
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
						{properties.map((property) => (
							<ListingCard
								key={property.id}
								data={property}
								token={user.token}
								onAction={handleDelete}
								actionID={property.id}
								actionLabel='Delete property'
							/>
						))}
					</div>
				</Fragment>
			)}
		</Container>
	);
};

export default Properties;
