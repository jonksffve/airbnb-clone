import { Fragment, useMemo, useState } from 'react';
import Container from '../components/UIhelpers/Container';
import Heading from '../components/Modals/Heading';
import IsEmpty from '../components/Listings/IsEmpty';
import ListingCard from '../components/Listings/ListingCard';
import { getFavoritesAPI } from '../api/AuthAPI';
import { useSelector } from 'react-redux';
import Spinner from '../components/UIhelpers/Spinner';

const Favorites = () => {
	const user = useSelector((state) => state.user);
	const [favorites, setFavorites] = useState([]);
	const [isLoading, setIsLoading] = useState(undefined);
	const [isEmpty, setIsEmpty] = useState(undefined);

	useMemo(async () => {
		if (!user.token) return;
		await getFavoritesAPI(user.token, setFavorites, setIsLoading, setIsEmpty);
	}, [user.token]);

	if (isEmpty) {
		return <IsEmpty />;
	}

	return (
		<Container>
			{isLoading && <Spinner />}
			{!isLoading && (
				<Fragment>
					<Heading
						title='All your favorited listings'
						subtitle='All those magic places you wish (or have) visited'
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
						{favorites.map((favorite) => (
							<ListingCard
								key={favorite.id}
								data={favorite.listing}
								token={user.token}
							/>
						))}
					</div>
				</Fragment>
			)}
		</Container>
	);
};

export default Favorites;
