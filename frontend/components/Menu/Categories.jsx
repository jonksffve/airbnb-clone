import ContainerMenu from '../UIhelpers/ContainerMenu';
import CategoryBox from './CategoryBox';
import { useSearchParams } from 'react-router-dom';
import { getCategories } from '../../hooks/Categories';

const Categories = () => {
	const [searchParams, setSearchParams] = useSearchParams();
	const category = searchParams.get('category');
	const categories = getCategories();

	return (
		<ContainerMenu>
			<div
				className='flex 
            flex-row 
            items-center
            justify-between
            overflow-x-auto
            pt-4'
			>
				{categories.map((item) => (
					<CategoryBox
						key={item.label}
						label={item.label}
						selected={category === item.label}
						icon={item.icon}
					/>
				))}
			</div>
		</ContainerMenu>
	);
};

export default Categories;
