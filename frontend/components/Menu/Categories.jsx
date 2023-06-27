import Container from '../UIhelpers/Container';
import { TbBeach } from 'react-icons/tb';

export const categories = [
	{
		label: 'Beach',
		icon: TbBeach,
		description: 'This property is close to the beach!',
	},
];

const Categories = () => {
	return (
		<Container>
			<div
				className='flex 
            flex-row 
            items-center
            justify-between
            overflow-x-auto
            pt-4'
			></div>
		</Container>
	);
};

export default Categories;
