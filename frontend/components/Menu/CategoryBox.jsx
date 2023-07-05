import { useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';

const CategoryBox = ({ icon: Icon, label, selected }) => {
	const [searchParams, setSearchParams] = useSearchParams();

	const handleClick = useCallback(() => {
		if (searchParams.get('category') === label) {
			searchParams.delete('category');
		}

		setSearchParams((prevState) => {
			prevState.set('category', label);
			return prevState;
		});
	}, [label, setSearchParams, searchParams]);

	return (
		<div
			onClick={handleClick}
			className={`flex
            cursor-pointer
            flex-col
            items-center
            justify-center
            gap-2
            border-b-2
            p-3
            transition
            hover:text-neutral-800
            ${selected ? 'border-b-neutral-800' : 'border-transparent'}
            ${selected ? 'text-neutral-800' : 'text-neutral-500'}
            `}
		>
			<Icon size={26} />
			<div className='text-sm font-medium'>{label}</div>
		</div>
	);
};

export default CategoryBox;
