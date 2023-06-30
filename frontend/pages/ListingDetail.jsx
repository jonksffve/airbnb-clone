import { useParams } from 'react-router-dom';

const ListingDetail = () => {
	const { id } = useParams();

	return (
		<div className='pt-40'>
			<h2>This is a detail page for item {id}</h2>
		</div>
	);
};

export default ListingDetail;
